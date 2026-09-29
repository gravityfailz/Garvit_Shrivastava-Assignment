package com.amexlumi.beam.parser;

import com.amexlumi.beam.model.EmployeeRecord;
import com.amexlumi.beam.model.ParsedRecord;
import com.amexlumi.beam.security.FieldEncryptor;
import com.amexlumi.beam.validation.EmployeeValidator;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;

import java.io.IOException;
import java.io.Reader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class CsvParser {

    private CsvParser() {
        // Utility class.
    }

    /**
     * Production entry point.
     *
     * Uses FIELD_ENCRYPTION_KEY from the environment.
     */
    public static List<ParsedRecord> parse(Path filePath)
            throws IOException {

        FieldEncryptor encryptor =
                new FieldEncryptor();

        return parse(filePath, encryptor);
    }

    /**
     * Testable entry point.
     *
     * Allows tests to provide a temporary Fernet key instead
     * of requiring the real production environment variable.
     */
    public static List<ParsedRecord> parse(
            Path filePath,
            FieldEncryptor encryptor) throws IOException {

        if (filePath == null) {
            throw new IllegalArgumentException(
                    "CSV file path must not be null"
            );
        }

        if (encryptor == null) {
            throw new IllegalArgumentException(
                    "FieldEncryptor must not be null"
            );
        }

        if (!Files.exists(filePath)) {
            throw new IOException(
                    "CSV source file does not exist: " + filePath
            );
        }

        if (!Files.isRegularFile(filePath)) {
            throw new IOException(
                    "CSV source path is not a regular file: " + filePath
            );
        }

        List<ParsedRecord> results =
                new ArrayList<>();

        try (Reader reader =
                     Files.newBufferedReader(
                             filePath,
                             StandardCharsets.UTF_8
                     );
             CSVParser parser =
                     CSVFormat.DEFAULT.builder()
                             .setHeader()
                             .setSkipHeaderRecord(true)
                             .setIgnoreEmptyLines(true)
                             .build()
                             .parse(reader)) {

            for (CSVRecord csvRecord : parser) {

                ParsedRecord parsedRecord =
                        parseRecord(csvRecord, encryptor);

                results.add(parsedRecord);
            }
        }

        return results;
    }

    /**
     * Parses one CSV record.
     *
     * A structurally malformed record is converted into an
     * error record instead of failing the complete ingestion.
     */
    private static ParsedRecord parseRecord(
            CSVRecord csvRecord,
            FieldEncryptor encryptor) {

        try {

            Map<String, Object> rawRecord =
                    convertRecord(csvRecord);

            /*
             * Validate the original CSV values before
             * normalization and encryption.
             */
            List<String> violations =
                    EmployeeValidator.validate(rawRecord);

            if (!violations.isEmpty()) {

                /*
                 * Keep invalid records in their original form
                 * so the error output contains the source data.
                 */
                return ParsedRecord.error(
                        rawRecord,
                        violations
                );
            }

            /*
             * null/empty CSV values become a single space.
             */
            Map<String, Object> normalizedRecord =
                    normalizeRecord(rawRecord);

            EmployeeRecord employeeRecord =
                    new EmployeeRecord(normalizedRecord);

            /*
             * Encrypt sensitive fields only after validation
             * and normalization.
             */
            EmployeeRecord encryptedRecord =
                    encryptor.encryptEmployeeRecord(
                            employeeRecord
                    );

            return ParsedRecord.valid(
                    encryptedRecord
            );

        } catch (IllegalArgumentException exception) {

            /*
             * A structurally malformed CSV row must not fail
             * the complete ingestion.
             */
            Map<String, Object> sourceRecord =
                    createMalformedRecord(csvRecord);

            List<String> violations =
                    List.of(
                            "Malformed CSV record at line "
                                    + csvRecord.getRecordNumber()
                                    + ": "
                                    + exception.getMessage()
                    );

            return ParsedRecord.error(
                    sourceRecord,
                    violations
            );
        }
    }

    private static Map<String, Object> convertRecord(
            CSVRecord csvRecord) {

        Map<String, Object> record =
                new LinkedHashMap<>();

        for (String header :
                csvRecord.getParser().getHeaderNames()) {

            String value = null;

            if (csvRecord.isMapped(header)) {
                value = csvRecord.get(header);
            }

            record.put(
                    header,
                    value
            );
        }

        return record;
    }

    /**
     * Creates a source representation for a structurally
     * malformed CSV record.
     *
     * We preserve the values that Commons CSV successfully
     * parsed and expose missing columns as null.
     */
    private static Map<String, Object> createMalformedRecord(
            CSVRecord csvRecord) {

        Map<String, Object> record =
                new LinkedHashMap<>();

        List<String> headers =
                csvRecord.getParser().getHeaderNames();

        for (int index = 0;
             index < headers.size();
             index++) {

            String header =
                    headers.get(index);

            Object value =
                    index < csvRecord.size()
                            ? csvRecord.get(index)
                            : null;

            record.put(
                    header,
                    value
            );
        }

        return record;
    }

    private static Map<String, Object> normalizeRecord(
            Map<String, Object> rawRecord) {

        Map<String, Object> normalized =
                new LinkedHashMap<>();

        for (Map.Entry<String, Object> entry :
                rawRecord.entrySet()) {

            Object value =
                    entry.getValue();

            if (value == null) {

                normalized.put(
                        entry.getKey(),
                        " "
                );

            } else if (value instanceof String
                    && ((String) value).isEmpty()) {

                normalized.put(
                        entry.getKey(),
                        " "
                );

            } else {

                normalized.put(
                        entry.getKey(),
                        value
                );
            }
        }

        return normalized;
    }
}

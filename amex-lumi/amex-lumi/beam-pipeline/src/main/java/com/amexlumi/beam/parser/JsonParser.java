package com.amexlumi.beam.parser;

import com.amexlumi.beam.model.EmployeeRecord;
import com.amexlumi.beam.model.ParsedRecord;
import com.amexlumi.beam.security.FieldEncryptor;
import com.amexlumi.beam.validation.EmployeeValidator;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class JsonParser {

    private static final ObjectMapper OBJECT_MAPPER =
            new ObjectMapper();

    private JsonParser() {
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
     * Allows a caller to provide a FieldEncryptor,
     * so tests do not need the real production encryption key.
     */
    public static List<ParsedRecord> parse(
            Path filePath,
            FieldEncryptor encryptor) throws IOException {

        if (filePath == null) {
            throw new IllegalArgumentException(
                    "JSON file path must not be null"
            );
        }

        if (encryptor == null) {
            throw new IllegalArgumentException(
                    "FieldEncryptor must not be null"
            );
        }

        if (!Files.exists(filePath)) {
            throw new IOException(
                    "JSON source file does not exist: " + filePath
            );
        }

        if (!Files.isRegularFile(filePath)) {
            throw new IOException(
                    "JSON source path is not a regular file: " + filePath
            );
        }

        String json = Files.readString(
                filePath,
                StandardCharsets.UTF_8
        );

        /*
         * Support UTF-8 BOM-byte order mark.
         */
        if (!json.isEmpty() && json.charAt(0) == '\uFEFF') {
            json = json.substring(1);
        }

        /*
         * An empty JSON document cannot produce a valid record.
         *
         * Treat it as an ingestion error instead of allowing
         * the entire Beam/Airflow execution to fail.
         */
        if (json.isBlank()) {

            return List.of(
                    createFileLevelErrorRecord(
                            filePath,
                            json,
                            "JSON source file is empty"
                    )
            );
        }

        List<Map<String, Object>> records;

        /*
         * ---------------------------------------------------------
         * JSON DOCUMENT PARSING
         * ---------------------------------------------------------
         *
         * A syntactically malformed JSON document must become an
         * error record instead of failing the complete ingestion.
         */
        try {

            records = readRecords(json);

        } catch (JsonProcessingException exception) {

            return List.of(
                    createFileLevelErrorRecord(
                            filePath,
                            json,
                            "Malformed JSON: "
                                    + exception.getOriginalMessage()
                    )
            );

        } catch (IOException exception) {

            return List.of(
                    createFileLevelErrorRecord(
                            filePath,
                            json,
                            "Unable to parse JSON: "
                                    + exception.getMessage()
                    )
            );
        }

        List<ParsedRecord> results =
                new ArrayList<>();

        /*
         * ---------------------------------------------------------
         * RECORD PROCESSING
         * ---------------------------------------------------------
         *
         * Each individual record is handled independently.
         *
         * A bad record does not stop the remaining records.
         */
        for (Map<String, Object> rawRecord : records) {

            if (rawRecord == null) {

                results.add(
                        ParsedRecord.error(
                                new LinkedHashMap<>(),
                                List.of(
                                        "record: record is null"
                                )
                        )
                );

                continue;
            }

            try {

                EmployeeRecord employeeRecord =
                        new EmployeeRecord(rawRecord);

                /*
                 * Validate the original source values first.
                 *
                 * This is important because encrypted values are
                 * much longer than the original phone/salary values
                 * and must not be used for validation.
                 */
                List<String> violations =
                        EmployeeValidator.validate(
                                employeeRecord
                        );

                if (!violations.isEmpty()) {

                    /*
                     * Invalid records remain unencrypted so that the
                     * original source record and validation violations
                     * can be written to the error output.
                     */
                    results.add(
                            ParsedRecord.error(
                                    rawRecord,
                                    violations
                            )
                    );

                    continue;
                }

                /*
                 * Only valid records are encrypted.
                 *
                 * FieldEncryptor handles:
                 *   - phone_number
                 *   - salary
                 *   - emergency_contact.phone
                 *   - emergency_contact_phone
                 */
                EmployeeRecord encryptedRecord =
                        encryptor.encryptEmployeeRecord(
                                employeeRecord
                        );

                results.add(
                        ParsedRecord.valid(
                                encryptedRecord
                        )
                );

            } catch (RuntimeException exception) {

                /*
                 * A single problematic record must not terminate
                 * the complete ingestion.
                 */
                results.add(
                        ParsedRecord.error(
                                rawRecord,
                                List.of(
                                        "Unable to process JSON record: "
                                                + exception.getMessage()
                                )
                        )
                );
            }
        }

        return results;
    }

    /**
     * Reads a JSON document containing either:
     *
     * 1. An array of employee objects.
     * 2. A single employee object.
     */
    private static List<Map<String, Object>> readRecords(
            String json) throws IOException {

        String trimmed = json.trim();

        /*
         * JSON array:
         *
         * [
         *   {
         *      "employee_id": "E000001"
         *   }
         * ]
         */
        if (trimmed.startsWith("[")) {

            return OBJECT_MAPPER.readValue(
                    trimmed,
                    new TypeReference<List<Map<String, Object>>>() {
                    }
            );
        }

        /*
         * Single JSON object:
         *
         * {
         *   "employee_id": "E000001"
         * }
         */
        if (trimmed.startsWith("{")) {

            Map<String, Object> record =
                    OBJECT_MAPPER.readValue(
                            trimmed,
                            new TypeReference<Map<String, Object>>() {
                            }
                    );

            return List.of(record);
        }

        /*
         * Anything else is an invalid JSON root.
         */
        throw new IOException(
                "JSON root must be an object or an array"
        );
    }

    /**
     * Creates an error record for a JSON document that could not
     * be parsed into individual employee records.
     *
     * Since the JSON structure itself is invalid, there may not be
     * a reliable individual source record. Therefore the original
     * source path and raw JSON are preserved in the source_record
     * map for troubleshooting.
     */
    private static ParsedRecord createFileLevelErrorRecord(
            Path filePath,
            String rawJson,
            String violation) {

        Map<String, Object> sourceRecord =
                new LinkedHashMap<>();

        sourceRecord.put(
                "source_file",
                filePath.toString()
        );

        sourceRecord.put(
                "raw_content",
                rawJson
        );

        return ParsedRecord.error(
                sourceRecord,
                List.of(violation)
        );
    }
}

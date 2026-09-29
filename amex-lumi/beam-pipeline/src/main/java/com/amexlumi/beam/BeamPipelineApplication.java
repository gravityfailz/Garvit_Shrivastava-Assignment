package com.amexlumi.beam;

import com.amexlumi.beam.model.IngestionRecord;
import com.amexlumi.beam.model.ParsedRecord;
import com.amexlumi.beam.parser.CsvParser;
import com.amexlumi.beam.parser.JsonParser;
import com.amexlumi.beam.parser.XmlParser;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.coders.SerializableCoder;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.transforms.Create;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.Filter;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.values.PCollection;
import org.apache.beam.sdk.values.TypeDescriptor;
import org.apache.beam.sdk.values.TypeDescriptors;
import org.postgresql.util.PGobject;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.UUID;

public final class BeamPipelineApplication {
    private static final ObjectMapper MAPPER = new ObjectMapper();
    private static final int BATCH_SIZE = 100;
    private static final String INSERT_SQL = """
            INSERT INTO ingested_records
                (execution_id, source_format, source_file,
                 source_creation_time, ingestion_timestamp, payload)
            VALUES (?, ?, ?, ?, ?, ?)
            """;

    private BeamPipelineApplication() { }

    public static void main(String[] args) {
        PipelineArguments a = PipelineArguments.parse(args);

        String executionId = a.executionId();
        String sourceFile = a.filePath();
        String postgresDsn = a.postgresDsn();
        String errorOutput = a.errorOutputPath();

        PipelineOptions options = PipelineOptionsFactory.create();
        Pipeline pipeline = Pipeline.create(options);

        PCollection<ParsedRecord> parsed = pipeline
                .apply("CreateInput", Create.of(sourceFile))
                .apply("ParseSource", ParDo.of(new ParseSourceFileFn()))
                .setCoder(SerializableCoder.of(ParsedRecord.class));

        parsed
                .apply("FilterErrors", Filter.by(ParsedRecord::isError))
                .apply("FormatErrors",
                        MapElements.into(TypeDescriptors.strings())
                                .via(BeamPipelineApplication::formatError))
                .apply("WriteErrors",
                        TextIO.write()
                                .to(errorOutput)
                                .withSuffix(".txt")
                                .withoutSharding());

        PCollection<IngestionRecord> valid = parsed
                .apply("FilterValid", Filter.by(ParsedRecord::isValid))
                .apply("CreateIngestionRecord",
                        MapElements.into(TypeDescriptor.of(IngestionRecord.class))
                                .via(record -> toIngestionRecord(
                                        record, executionId, sourceFile)))
                .setCoder(SerializableCoder.of(IngestionRecord.class));

        valid.apply("WriteToPostgres",
                ParDo.of(new WriteValidRecordToPostgres(postgresDsn)));

        pipeline.run().waitUntilFinish();

        System.out.println("LUMI: Ingestion completed successfully.");
    }

    /** Parses CSV, JSON, or XML inside an actual Beam DoFn. */
    public static final class ParseSourceFileFn extends DoFn<String, ParsedRecord> {
        @ProcessElement
        public void processElement(ProcessContext context) throws IOException {
            Path path = Path.of(context.element());
            String name = path.getFileName().toString().toLowerCase(Locale.ROOT);
            List<ParsedRecord> records;

            if (name.endsWith(".csv")) records = CsvParser.parse(path);
            else if (name.endsWith(".json")) records = JsonParser.parse(path);
            else if (name.endsWith(".xml")) records = XmlParser.parse(path);
            else throw new IllegalArgumentException("No parser registered for: " + name);

            for (ParsedRecord record : records) {
                if (record != null) context.output(record);
            }
        }
    }

    private static IngestionRecord toIngestionRecord(
            ParsedRecord record, String executionId, String sourceFile) {
        if (record.getEmployeeRecord() == null) {
            throw new IllegalStateException("Valid ParsedRecord contains null EmployeeRecord");
        }
        Instant now = Instant.now();
        return new IngestionRecord(
                executionId,
                sourceFormat(sourceFile),
                sourceFile,
                now,
                Instant.now(),
                record.getEmployeeRecord().toMap());
    }

    private static String sourceFormat(String sourceFile) {
        String name = Path.of(sourceFile).getFileName().toString().toLowerCase(Locale.ROOT);
        if (name.endsWith(".csv")) return "CSV";
        if (name.endsWith(".json")) return "JSON";
        if (name.endsWith(".xml")) return "XML";
        throw new IllegalArgumentException("Unsupported source format: " + sourceFile);
    }

    private static String formatError(ParsedRecord record) {
        try {
            return MAPPER.writeValueAsString(
                    new ErrorDetail(record.getSourceRecord(), record.getViolations()));
        } catch (JsonProcessingException e) {
            throw new IllegalStateException("Unable to serialize error record", e);
        }
    }

    /** Beam sink: one JDBC connection per DoFn instance, batched writes, transaction per batch. */
    public static final class WriteValidRecordToPostgres extends DoFn<IngestionRecord, Void> {
        private final String postgresDsn;
        private transient Connection connection;
        private transient PreparedStatement statement;
        private transient int batchCount;

        public WriteValidRecordToPostgres(String postgresDsn) {
            if (postgresDsn == null || postgresDsn.isBlank()) {
                throw new IllegalArgumentException("PostgreSQL DSN must not be null or empty");
            }
            this.postgresDsn = postgresDsn.trim();
        }

        @Setup
        public void setup() throws SQLException {
            connection = DriverManager.getConnection(toJdbcUrl(postgresDsn));
            connection.setAutoCommit(false);
            statement = connection.prepareStatement(INSERT_SQL);
            batchCount = 0;
        }

        @ProcessElement
        public void processElement(ProcessContext context) throws SQLException {
            IngestionRecord record = context.element();
            if (record == null) return;

            statement.setObject(1, UUID.fromString(record.getExecutionId()));
            statement.setString(2, record.getSourceFormat());
            statement.setString(3, record.getSourceFile());
            statement.setTimestamp(4, timestamp(record.getSourceCreationTime()));
            statement.setTimestamp(5, timestamp(record.getIngestionTimestamp()));

            PGobject json = new PGobject();
            json.setType("jsonb");
            try {
                json.setValue(MAPPER.writeValueAsString(record.getPayload()));
            } catch (JsonProcessingException e) {
                throw new IllegalStateException("Unable to serialize employee payload", e);
            }
            statement.setObject(6, json);
            statement.addBatch();
            batchCount++;

            if (batchCount >= BATCH_SIZE) flushBatch();
        }

        @FinishBundle
        public void finishBundle() throws SQLException { flushBatch(); }

        @Teardown
        public void teardown() {
            try { if (statement != null) statement.close(); }
            catch (SQLException ignored) { }
            try { if (connection != null) connection.close(); }
            catch (SQLException ignored) { }
        }

        private void flushBatch() throws SQLException {
            if (batchCount == 0) return;
            try {
                statement.executeBatch();
                connection.commit();
                statement.clearBatch();
                batchCount = 0;
            } catch (SQLException e) {
                connection.rollback();
                throw e;
            }
        }
    }

    private static java.sql.Timestamp timestamp(Instant instant) {
        return java.sql.Timestamp.valueOf(
                LocalDateTime.ofInstant(instant, ZoneOffset.UTC));
    }

    private static String toJdbcUrl(String dsn) {
        String value = dsn.trim();
        if (value.startsWith("jdbc:postgresql://")) return value;
        if (!value.startsWith("postgresql://")) {
            throw new IllegalArgumentException("Unsupported PostgreSQL DSN format: " + dsn);
        }

        String rest = value.substring("postgresql://".length());
        int at = rest.indexOf('@');
        if (at < 0) throw new IllegalArgumentException("PostgreSQL DSN is missing credentials");

        String credentials = rest.substring(0, at);
        String hostAndDatabase = rest.substring(at + 1);
        int colon = credentials.indexOf(':');
        if (colon < 0) throw new IllegalArgumentException("PostgreSQL DSN is missing password");

        String user = credentials.substring(0, colon);
        String password = credentials.substring(colon + 1);
        return "jdbc:postgresql://" + hostAndDatabase
                + "?user=" + encode(user) + "&password=" + encode(password);
    }

    private static String encode(String value) {
        return value.replace("%", "%25")
                .replace(" ", "%20")
                .replace("&", "%26")
                .replace("=", "%3D")
                .replace("?", "%3F");
    }

    private record ErrorDetail(Map<String, Object> source_record, List<String> violations) { }

    private record PipelineArguments(
            String filePath, String executionId,
            String postgresDsn, String errorOutputPath) {
/*This is configuration object for the beam application */
        static PipelineArguments parse(String[] args) {
            String file = null, id = null, dsn = null, error = null;
            for (int i = 0; i < args.length; i++) {
                String arg = args[i];
                switch (arg) {
                    case "--file_path" -> file = require(args, ++i, arg);
                    case "--execution_id" -> id = require(args, ++i, arg);
                    case "--postgres_dsn" -> dsn = require(args, ++i, arg);
                    case "--error_output_path" -> error = require(args, ++i, arg);
                    default -> throw new IllegalArgumentException("Unknown argument: " + arg);
                }
            }
            if (file == null || file.isBlank()) throw new IllegalArgumentException("--file_path is required");
            if (id == null || id.isBlank()) throw new IllegalArgumentException("--execution_id is required");
            if (dsn == null || dsn.isBlank()) dsn = System.getenv("LUMI_POSTGRES_DSN");
            if (dsn == null || dsn.isBlank()) throw new IllegalArgumentException("--postgres_dsn is required or LUMI_POSTGRES_DSN must be set");
            if (error == null || error.isBlank()) throw new IllegalArgumentException("--error_output_path is required");
            UUID.fromString(id);
            if (!Files.isRegularFile(Path.of(file))) throw new IllegalArgumentException("Input file does not exist: " + file);
            return new PipelineArguments(file, id, dsn, error);
        }

        private static String require(String[] args, int index, String arg) {
            if (index >= args.length || args[index] == null || args[index].isBlank() || args[index].startsWith("--")) {
                throw new IllegalArgumentException("Missing value for " + arg);
            }
            return args[index];
        }
    }
}


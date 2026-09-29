package com.amexlumi.ingestion.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.macasaet.fernet.Key;
import com.macasaet.fernet.StringValidator;
import com.macasaet.fernet.Token;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.net.URI;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.Duration;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@Service
public class IngestedDataService {

    private static final String FIELD_ENCRYPTION_KEY =
            "FIELD_ENCRYPTION_KEY";

    private final ObjectMapper objectMapper;
    private final String postgresDsn;
    private final Key encryptionKey;

    public IngestedDataService(
            ObjectMapper objectMapper,
            @Value("${lumi.postgres-dsn}")
            String postgresDsn) {

        this.objectMapper = objectMapper;
        this.postgresDsn = postgresDsn;

        String encryptionKeyValue =
                System.getenv(
                        FIELD_ENCRYPTION_KEY
                );

        if (encryptionKeyValue == null
                || encryptionKeyValue.isBlank()) {

            throw new IllegalStateException(
                    "FIELD_ENCRYPTION_KEY environment variable "
                            + "is missing or empty."
            );
        }

        try {
            this.encryptionKey =
                    new Key(
                            encryptionKeyValue.trim()
                    );

        } catch (RuntimeException exception) {

            throw new IllegalStateException(
                    "FIELD_ENCRYPTION_KEY is not a valid "
                            + "Fernet key.",
                    exception
            );
        }
    }

    public Map<String, Object> getDecryptedData(
            String executionId) {

        if (executionId == null
                || executionId.isBlank()) {

            throw new IllegalArgumentException(
                    "execution_id is required."
            );
        }

        String sql =
                """
                SELECT
                    execution_id,
                    source_format,
                    source_file,
                    source_creation_time,
                    ingestion_timestamp,
                    payload
                FROM ingested_records
                WHERE execution_id = ?
                ORDER BY id
                """;

        List<JsonNode> records =
                new ArrayList<>();

        String actualExecutionId = null;

        try (
                Connection connection =
                        createConnection();

                PreparedStatement statement =
                        connection.prepareStatement(sql)
        ) {

            statement.setObject(
                    1,
                    java.util.UUID.fromString(
                            executionId
                    )
            );

            try (
                    ResultSet resultSet =
                            statement.executeQuery()
            ) {

                while (resultSet.next()) {

                    actualExecutionId =
                            resultSet.getObject(
                                    "execution_id"
                            ).toString();

                    String payload =
                            resultSet.getString(
                                    "payload"
                            );

                    JsonNode payloadNode =
                            objectMapper.readTree(
                                    payload
                            );

                    decryptPayload(
                            payloadNode
                    );

                    records.add(
                            payloadNode
                    );
                }
            }

        } catch (IllegalArgumentException exception) {

            throw new IllegalArgumentException(
                    "execution_id must be a valid UUID.",
                    exception
            );

        } catch (SQLException exception) {

            throw new IllegalStateException(
                    "Unable to retrieve ingested records "
                            + "from PostgreSQL.",
                    exception
            );

        } catch (Exception exception) {

            throw new IllegalStateException(
                    "Unable to read or decrypt ingested records.",
                    exception
            );
        }

        Map<String, Object> response =
                new LinkedHashMap<>();

        response.put(
                "execution_id",
                actualExecutionId != null
                        ? actualExecutionId
                        : executionId
        );

        response.put(
                "record_count",
                records.size()
        );

        response.put(
                "records",
                records
        );

        return response;
    }

    private void decryptPayload(
            JsonNode payloadNode) {

        if (!(payloadNode instanceof ObjectNode objectNode)) {
            return;
        }

        decryptTopLevelField(
                objectNode,
                "phone_number"
        );

        decryptTopLevelField(
                objectNode,
                "salary"
        );

        decryptTopLevelField(
                objectNode,
                "emergency_contact_phone"
        );

        decryptNestedPhone(
                objectNode
        );
    }

    private void decryptTopLevelField(
            ObjectNode record,
            String fieldName) {

        JsonNode field =
                record.get(fieldName);

        if (field == null
                || field.isNull()
                || !field.isTextual()) {

            return;
        }

        String encryptedValue =
                field.asText();

        if (encryptedValue.isBlank()) {
            return;
        }

        record.put(
                fieldName,
                decrypt(encryptedValue)
        );
    }

    private void decryptNestedPhone(
            ObjectNode record) {

        JsonNode emergencyContact =
                record.get(
                        "emergency_contact"
                );

        if (!(emergencyContact instanceof ObjectNode contact)) {
            return;
        }

        JsonNode phone =
                contact.get("phone");

        if (phone == null
                || phone.isNull()
                || !phone.isTextual()) {

            return;
        }

        String encryptedPhone =
                phone.asText();

        if (encryptedPhone.isBlank()) {
            return;
        }

        contact.put(
                "phone",
                decrypt(encryptedPhone)
        );
    }

    private String decrypt(
            String encryptedValue) {

        try {

            Token token =
                    Token.fromString(
                            encryptedValue
                    );

            return token.validateAndDecrypt(
                    encryptionKey,
                    new StringValidator() {

                        @Override
                        public Duration getTimeToLive() {
                            return Duration.ofDays(
                                    3650
                            );
                        }
                    }
            );

        } catch (RuntimeException exception) {

            throw new IllegalStateException(
                    "Unable to decrypt an encrypted field.",
                    exception
            );
        }
    }

    private Connection createConnection()
            throws SQLException {

        URI uri =
                URI.create(
                        postgresDsn
                );

        if (!"postgresql".equalsIgnoreCase(
                uri.getScheme()
        )) {

            throw new IllegalStateException(
                    "LUMI_POSTGRES_DSN must use "
                            + "the postgresql:// scheme."
            );
        }

        String userInfo =
                uri.getRawUserInfo();

        if (userInfo == null
                || !userInfo.contains(":")) {

            throw new IllegalStateException(
                    "LUMI_POSTGRES_DSN must contain "
                            + "database username and password."
            );
        }

        int separator =
                userInfo.indexOf(':');

        String username =
                URLDecoder.decode(
                        userInfo.substring(
                                0,
                                separator
                        ),
                        StandardCharsets.UTF_8
                );

        String password =
                URLDecoder.decode(
                        userInfo.substring(
                                separator + 1
                        ),
                        StandardCharsets.UTF_8
                );

        String path =
                uri.getRawPath();

        if (path == null
                || path.isBlank()) {

            throw new IllegalStateException(
                    "LUMI_POSTGRES_DSN must contain "
                            + "a database name."
            );
        }

        StringBuilder jdbcUrl =
                new StringBuilder();

        jdbcUrl.append(
                "jdbc:postgresql://"
        );

        jdbcUrl.append(
                uri.getHost()
        );

        if (uri.getPort() != -1) {

            jdbcUrl.append(":");
            jdbcUrl.append(
                    uri.getPort()
            );
        }

        jdbcUrl.append(
                path
        );

        if (uri.getRawQuery() != null
                && !uri.getRawQuery().isBlank()) {

            jdbcUrl.append("?")
                    .append(
                            uri.getRawQuery()
                    );
        }

        return DriverManager.getConnection(
                jdbcUrl.toString(),
                username,
                password
        );
    }
}

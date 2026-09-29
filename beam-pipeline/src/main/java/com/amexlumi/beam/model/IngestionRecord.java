package com.amexlumi.beam.model;

import java.io.Serializable;
import java.time.Instant;
import java.util.LinkedHashMap;
import java.util.Map;

public class IngestionRecord implements Serializable {

    private static final long serialVersionUID = 1L;

    private final String executionId;
    private final String sourceFormat;
    private final String sourceFile;
    private final Instant sourceCreationTime;
    private final Instant ingestionTimestamp;
    private final Map<String, Object> payload;

    public IngestionRecord(
            String executionId,
            String sourceFormat,
            String sourceFile,
            Instant sourceCreationTime,
            Instant ingestionTimestamp,
            Map<String, Object> payload) {

        if (executionId == null || executionId.isBlank()) {
            throw new IllegalArgumentException(
                    "executionId must not be null or empty"
            );
        }

        if (sourceFormat == null || sourceFormat.isBlank()) {
            throw new IllegalArgumentException(
                    "sourceFormat must not be null or empty"
            );
        }

        if (sourceFile == null || sourceFile.isBlank()) {
            throw new IllegalArgumentException(
                    "sourceFile must not be null or empty"
            );
        }

        if (sourceCreationTime == null) {
            throw new IllegalArgumentException(
                    "sourceCreationTime must not be null"
            );
        }

        if (ingestionTimestamp == null) {
            throw new IllegalArgumentException(
                    "ingestionTimestamp must not be null"
            );
        }

        if (payload == null) {
            throw new IllegalArgumentException(
                    "payload must not be null"
            );
        }

        this.executionId = executionId;
        this.sourceFormat = sourceFormat;
        this.sourceFile = sourceFile;
        this.sourceCreationTime = sourceCreationTime;
        this.ingestionTimestamp = ingestionTimestamp;
        this.payload = new LinkedHashMap<>(payload);
    }

    public String getExecutionId() {
        return executionId;
    }

    public String getSourceFormat() {
        return sourceFormat;
    }

    public String getSourceFile() {
        return sourceFile;
    }

    public Instant getSourceCreationTime() {
        return sourceCreationTime;
    }

    public Instant getIngestionTimestamp() {
        return ingestionTimestamp;
    }

    public Map<String, Object> getPayload() {
        return new LinkedHashMap<>(payload);
    }

    public EmployeeRecord getEmployeeRecord() {
        return new EmployeeRecord(payload);
    }

    @Override
    public String toString() {
        return "IngestionRecord{" +
                "executionId='" + executionId + '\'' +
                ", sourceFormat='" + sourceFormat + '\'' +
                ", sourceFile='" + sourceFile + '\'' +
                ", sourceCreationTime=" + sourceCreationTime +
                ", ingestionTimestamp=" + ingestionTimestamp +
                ", payload=" + payload +
                '}';
    }
}

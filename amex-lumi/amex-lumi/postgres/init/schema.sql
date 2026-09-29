CREATE TABLE IF NOT EXISTS ingested_records (
    id                   BIGSERIAL PRIMARY KEY,
    execution_id         UUID        NOT NULL,
    source_format        VARCHAR(20) NOT NULL,
    source_file          TEXT        NOT NULL,
    source_creation_time TIMESTAMP   NOT NULL,
    ingestion_timestamp  TIMESTAMP   NOT NULL DEFAULT now(),
    payload              JSONB       NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_ingested_records_execution_id
    ON ingested_records (execution_id);

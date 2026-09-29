package com.amexlumi.ingestion.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;

@JsonInclude(JsonInclude.Include.NON_NULL)
public class IngestionResponse {

    @JsonProperty("execution_id")
    private final String executionId;

    @JsonProperty("dag_run_state")
    private final String dagRunState;

    @JsonProperty("file_split")
    private final Boolean fileSplit;

    @JsonProperty("part_count")
    private final Integer partCount;

    @JsonProperty("prepared_files")
    private final List<String> preparedFiles;

    public IngestionResponse(
            String executionId,
            String dagRunState) {

        this.executionId = executionId;
        this.dagRunState = dagRunState;
        this.fileSplit = null;
        this.partCount = null;
        this.preparedFiles = null;
    }

    public IngestionResponse(
            String executionId,
            String dagRunState,
            boolean fileSplit,
            int partCount,
            List<String> preparedFiles) {

        this.executionId = executionId;
        this.dagRunState = dagRunState;
        this.fileSplit = fileSplit;
        this.partCount = partCount;
        this.preparedFiles = preparedFiles;
    }

    public String getExecutionId() {
        return executionId;
    }

    public String getDagRunState() {
        return dagRunState;
    }

    public Boolean getFileSplit() {
        return fileSplit;
    }

    public Integer getPartCount() {
        return partCount;
    }

    public List<String> getPreparedFiles() {
        return preparedFiles;
    }
}

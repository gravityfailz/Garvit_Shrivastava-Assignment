package com.amexlumi.ingestion.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public class IngestionRequest {

    @JsonProperty("file_path")
    private String filePath;

    @JsonProperty("control_file_path")
    private String controlFilePath;

    public String getFilePath() {
        return filePath;
    }

    public void setFilePath(String filePath) {
        this.filePath = filePath;
    }

    public String getControlFilePath() {
        return controlFilePath;
    }

    public void setControlFilePath(String controlFilePath) {
        this.controlFilePath = controlFilePath;
    }
}

package com.amexlumi.ingestion.service;

import com.amexlumi.ingestion.config.AirflowProperties;
import com.amexlumi.ingestion.config.LumiProperties;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class AirflowDagTriggerService {

    private final RestTemplate airflowRestTemplate;

    private final AirflowProperties airflowProperties;

    private final LumiProperties lumiProperties;

    public AirflowDagTriggerService(
            RestTemplate airflowRestTemplate,
            AirflowProperties airflowProperties,
            LumiProperties lumiProperties) {

        this.airflowRestTemplate =
                airflowRestTemplate;

        this.airflowProperties =
                airflowProperties;

        this.lumiProperties =
                lumiProperties;
    }

    public String triggerIngestion(
            List<String> filePaths,
            String executionId,
            String controlFilePath,
            long expectedRecordCount) {

        if (filePaths == null
                || filePaths.isEmpty()) {

            throw new IllegalArgumentException(
                    "At least one file path is required."
            );
        }

        if (executionId == null
                || executionId.isBlank()) {

            throw new IllegalArgumentException(
                    "execution_id is required."
            );
        }

        if (controlFilePath == null
                || controlFilePath.isBlank()) {

            throw new IllegalArgumentException(
                    "control_file_path is required."
            );
        }

        if (expectedRecordCount < 0) {

            throw new IllegalArgumentException(
                    "expected_record_count must not be negative."
            );
        }

        String url =
                airflowProperties.getBaseUrl()
                        + "/api/v1/dags/"
                        + airflowProperties.getDagId()
                        + "/dagRuns";


// -----------aiflow object 
        Map<String, Object> conf =
                new HashMap<>();


        conf.put(
                "file_path",
                filePaths.get(0)
        );

        
        conf.put(
                "file_paths",
                filePaths
        );

        conf.put(
                "execution_id",
                executionId
        );

        conf.put(
                "postgres_dsn",
                lumiProperties.getPostgresDsn()
        );

       
        conf.put(
                "control_file_path",
                controlFilePath
        );

        conf.put(
                "expected_record_count",
                expectedRecordCount
        );

        
//  ------request body
        Map<String, Object> body =
                new HashMap<>();

        body.put(
                "dag_run_id",
                executionId
        );

        body.put(
                "conf",
                conf
        );

        HttpHeaders headers =
                new HttpHeaders();

        headers.setContentType(
                MediaType.APPLICATION_JSON
        );

        HttpEntity<Map<String, Object>> request =
                new HttpEntity<>(
                        body,
                        headers
                );

        ResponseEntity<Map> response =
                airflowRestTemplate.postForEntity(
                        url,
                        request,
                        Map.class
                );

        return response.getBody() != null
                ? String.valueOf(
                        response.getBody().get("state")
                )
                : "unknown";
    }

    public String getIngestionStatus(
            String executionId) {

        String url =
                airflowProperties.getBaseUrl()
                        + "/api/v1/dags/"
                        + airflowProperties.getDagId()
                        + "/dagRuns/"
                        + executionId;

        ResponseEntity<Map> response =
                airflowRestTemplate.getForEntity(
                        url,
                        Map.class
                );

        if (response.getBody() == null) {
            return "FAILED";
        }

        Object stateObject =
                response.getBody().get("state");

        if (stateObject == null) {
            return "FAILED";
        }

        String airflowState =
                String.valueOf(
                        stateObject
                ).toLowerCase();

        return normalizeAirflowState(
                airflowState
        );
    }

    private String normalizeAirflowState(
            String airflowState) {

        return switch (airflowState) {

            case "queued" ->
                    "QUEUED";

            case "running" ->
                    "RUNNING";

            case "success" ->
                    "COMPLETED";

            case "failed",
                 "upstream_failed",
                 "removed" ->
                    "FAILED";

            case "up_for_retry",
                 "up_for_reschedule",
                 "deferred" ->
                    "RUNNING";

            default ->
                    "RUNNING";
        };
    }
}

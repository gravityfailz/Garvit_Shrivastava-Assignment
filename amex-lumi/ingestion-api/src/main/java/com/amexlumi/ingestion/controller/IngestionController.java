package com.amexlumi.ingestion.controller;

import com.amexlumi.ingestion.dto.IngestionRequest;
import com.amexlumi.ingestion.dto.IngestionResponse;
import com.amexlumi.ingestion.service.AirflowDagTriggerService;
import com.amexlumi.ingestion.service.ControlFileService;
import com.amexlumi.ingestion.service.FilePreparationService;
import com.amexlumi.ingestion.service.IngestedDataService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClientException;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
public class IngestionController {

    private final AirflowDagTriggerService airflowDagTriggerService;
    private final FilePreparationService filePreparationService;
    private final ControlFileService controlFileService;
    private final IngestedDataService ingestedDataService;

    public IngestionController(
            AirflowDagTriggerService airflowDagTriggerService,
            FilePreparationService filePreparationService,
            ControlFileService controlFileService,
            IngestedDataService ingestedDataService) {

        this.airflowDagTriggerService =
                airflowDagTriggerService;

        this.filePreparationService =
                filePreparationService;

        this.controlFileService =
                controlFileService;

        this.ingestedDataService =
                ingestedDataService;
    }

    @PostMapping("/ingest")
    public ResponseEntity<?> ingest(
            @RequestBody IngestionRequest request) {

        if (request == null
                || request.getFilePath() == null
                || request.getFilePath().isBlank()) {

            return ResponseEntity
                    .badRequest()
                    .body("file_path is required");
        }

        if (request.getControlFilePath() == null
                || request.getControlFilePath().isBlank()) {

            return ResponseEntity
                    .badRequest()
                    .body("control_file_path is required");
        }

        String executionId =
                UUID.randomUUID().toString(); 

        try {

            long expectedRecordCount =
                    controlFileService.readExpectedRecordCount(
                            request.getControlFilePath()
                    );

            List<String> preparedFiles =
                    filePreparationService.prepareFiles(
                            request.getFilePath(),
                            executionId
                    );

            String dagRunState =
                    airflowDagTriggerService.triggerIngestion(
                            preparedFiles,
                            executionId,
                            request.getControlFilePath(),
                            expectedRecordCount
                    );

            boolean fileSplit =
                    !preparedFiles.isEmpty()
                            && (
                            preparedFiles.size() > 1
                                    || !preparedFiles.get(0)
                                    .equals(
                                            request.getFilePath()
                                    )
                    );

            int partCount =
                    preparedFiles.size();

            return ResponseEntity.ok(
                    new IngestionResponse(
                            executionId,
                            dagRunState,
                            fileSplit,
                            partCount,
                            preparedFiles
                    )
            );

        } catch (IllegalArgumentException ex) {

            return ResponseEntity
                    .badRequest()
                    .body(ex.getMessage());

        } catch (RestClientException ex) {

            return ResponseEntity
                    .status(502)
                    .body(
                            "Failed to trigger ingestion DAG: "
                                    + ex.getMessage()
                    );

        } catch (IllegalStateException ex) {

            return ResponseEntity
                    .status(500)
                    .body(ex.getMessage());
        }
    }

    @GetMapping("/ingest/{executionId}/status")
    public ResponseEntity<?> getIngestionStatus(
            @PathVariable String executionId) {

        if (executionId == null
                || executionId.isBlank()) {

            return ResponseEntity
                    .badRequest()
                    .body("execution_id is required");
        }

        try {

            String status =
                    airflowDagTriggerService.getIngestionStatus(
                            executionId
                    );

            return ResponseEntity.ok(
                    new IngestionResponse(
                            executionId,
                            status
                    )
            );

        } catch (RestClientException ex) {

            return ResponseEntity
                    .status(502)
                    .body(
                            "Failed to retrieve ingestion status: "
                                    + ex.getMessage()
                    );
        }
    }

    @GetMapping("/ingest/{executionId}/data")
    public ResponseEntity<?> getIngestedData(
            @PathVariable String executionId) {

        if (executionId == null
                || executionId.isBlank()) {

            return ResponseEntity
                    .badRequest()
                    .body("execution_id is required");
        }

        try {

            Map<String, Object> response =
                    ingestedDataService.getDecryptedData(
                            executionId
                    );

            return ResponseEntity.ok(
                    response
            );

        } catch (IllegalArgumentException ex) {

            return ResponseEntity
                    .badRequest()
                    .body(ex.getMessage());

        } catch (IllegalStateException ex) {

            return ResponseEntity
                    .status(500)
                    .body(ex.getMessage());
        }
    }
}

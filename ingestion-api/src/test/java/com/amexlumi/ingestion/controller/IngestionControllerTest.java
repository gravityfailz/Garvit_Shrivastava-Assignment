package com.amexlumi.ingestion.controller;

import com.amexlumi.ingestion.dto.IngestionRequest;
import com.amexlumi.ingestion.service.AirflowDagTriggerService;
import com.amexlumi.ingestion.service.ControlFileService;
import com.amexlumi.ingestion.service.FilePreparationService;
import com.amexlumi.ingestion.service.IngestedDataService;
import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class IngestionControllerTest {

    @Test
    void ingestShouldTriggerAirflowForPreparedFiles() {

        AirflowDagTriggerService airflowService =
                mock(AirflowDagTriggerService.class);

        FilePreparationService filePreparationService =
                mock(FilePreparationService.class);

        ControlFileService controlFileService =
                mock(ControlFileService.class);

        IngestedDataService ingestedDataService =
                mock(IngestedDataService.class);

        IngestionController controller =
                new IngestionController(
                        airflowService,
                        filePreparationService,
                        controlFileService,
                        ingestedDataService
                );

        IngestionRequest request =
                new IngestionRequest();

        request.setFilePath(
                "/opt/data/sample_data.csv"
        );

        request.setControlFilePath(
                "/opt/data/control/"
                        + "employee_ingestion_control.properties"
        );

        long expectedRecordCount = 10000L;

        when(
                controlFileService.readExpectedRecordCount(
                        eq(
                                "/opt/data/control/"
                                        + "employee_ingestion_control.properties"
                        )
                )
        ).thenReturn(expectedRecordCount);

        List<String> preparedFiles =
                List.of(
                        "/opt/data/split-output/"
                                + "part-001.csv",
                        "/opt/data/split-output/"
                                + "part-002.csv"
                );

        when(
                filePreparationService.prepareFiles(
                        eq(
                                "/opt/data/sample_data.csv"
                        ),
                        anyString()
                )
        ).thenReturn(preparedFiles);

        when(
                airflowService.triggerIngestion(
                        eq(preparedFiles),
                        anyString(),
                        eq(
                                "/opt/data/control/"
                                        + "employee_ingestion_control.properties"
                        ),
                        eq(expectedRecordCount)
                )
        ).thenReturn("queued");

        ResponseEntity<?> response =
                controller.ingest(request);

        assertEquals(
                200,
                response.getStatusCode().value()
        );

        assertTrue(
                response.getBody() != null
        );

        verify(
                controlFileService
        ).readExpectedRecordCount(
                eq(
                        "/opt/data/control/"
                                + "employee_ingestion_control.properties"
                )
        );

        verify(
                filePreparationService
        ).prepareFiles(
                eq(
                        "/opt/data/sample_data.csv"
                ),
                anyString()
        );

        verify(
                airflowService
        ).triggerIngestion(
                eq(preparedFiles),
                anyString(),
                eq(
                        "/opt/data/control/"
                                + "employee_ingestion_control.properties"
                ),
                eq(expectedRecordCount)
        );
    }

    @Test
    void ingestShouldReturnBadRequestWhenFilePathIsMissing() {

        AirflowDagTriggerService airflowService =
                mock(AirflowDagTriggerService.class);

        FilePreparationService filePreparationService =
                mock(FilePreparationService.class);

        ControlFileService controlFileService =
                mock(ControlFileService.class);

        IngestedDataService ingestedDataService =
                mock(IngestedDataService.class);

        IngestionController controller =
                new IngestionController(
                        airflowService,
                        filePreparationService,
                        controlFileService,
                        ingestedDataService
                );

        IngestionRequest request =
                new IngestionRequest();

        request.setFilePath("");

        ResponseEntity<?> response =
                controller.ingest(request);

        assertEquals(
                400,
                response.getStatusCode().value()
        );

        assertEquals(
                "file_path is required",
                response.getBody()
        );
    }

    @Test
    void ingestShouldReturnBadRequestWhenControlFilePathIsMissing() {

        AirflowDagTriggerService airflowService =
                mock(AirflowDagTriggerService.class);

        FilePreparationService filePreparationService =
                mock(FilePreparationService.class);

        ControlFileService controlFileService =
                mock(ControlFileService.class);

        IngestedDataService ingestedDataService =
                mock(IngestedDataService.class);

        IngestionController controller =
                new IngestionController(
                        airflowService,
                        filePreparationService,
                        controlFileService,
                        ingestedDataService
                );

        IngestionRequest request =
                new IngestionRequest();

        request.setFilePath(
                "/opt/data/sample_data.csv"
        );

        request.setControlFilePath("");

        ResponseEntity<?> response =
                controller.ingest(request);

        assertEquals(
                400,
                response.getStatusCode().value()
        );

        assertEquals(
                "control_file_path is required",
                response.getBody()
        );
    }
}

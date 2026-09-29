package com.amexlumi.ingestion.service;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ControlFileServiceTest {

    @TempDir
    Path temporaryDirectory;

    private Path controlDirectory;

    private ControlFileService controlFileService;

    @BeforeEach
    void setUp() throws IOException {

        controlDirectory =
                Files.createDirectory(
                        temporaryDirectory.resolve(
                                "control"
                        )
                );

        controlFileService =
                new ControlFileService(
                        temporaryDirectory.toString()
                );
    }

    @AfterEach
    void tearDown() throws IOException {

        /*
         * JUnit automatically removes the @TempDir
         * directory after each test.
         *
         * This method is intentionally empty.
         */
    }

    @Test
    void shouldReadValidRecordCount() throws IOException {

        Path controlFile =
                createControlFile(
                        "record_count=10000"
                );

        long result =
                controlFileService.readExpectedRecordCount(
                        controlFile.toString()
                );

        assertEquals(
                10000L,
                result
        );
    }

    @Test
    void shouldAcceptZeroRecordCount() throws IOException {

        Path controlFile =
                createControlFile(
                        "record_count=0"
                );

        long result =
                controlFileService.readExpectedRecordCount(
                        controlFile.toString()
                );

        assertEquals(
                0L,
                result
        );
    }

    @Test
    void shouldAcceptRecordCountWithWhitespace() throws IOException {

        Path controlFile =
                createControlFile(
                        "record_count= 10000 "
                );

        long result =
                controlFileService.readExpectedRecordCount(
                        controlFile.toString()
                );

        assertEquals(
                10000L,
                result
        );
    }

    @Test
    void shouldRejectDecimalRecordCount() throws IOException {

        Path controlFile =
                createControlFile(
                        "record_count=10000.5"
                );

        IllegalArgumentException exception =
                assertThrows(
                        IllegalArgumentException.class,
                        () ->
                                controlFileService
                                        .readExpectedRecordCount(
                                                controlFile.toString()
                                        )
                );

        assertEquals(
                true,
                exception.getMessage()
                        .contains(
                                "non-negative integer"
                        )
        );
    }

    @Test
    void shouldRejectDecimalRecordCountEndingWithZero()
            throws IOException {

        Path controlFile =
                createControlFile(
                        "record_count=9999.0"
                );

        IllegalArgumentException exception =
                assertThrows(
                        IllegalArgumentException.class,
                        () ->
                                controlFileService
                                        .readExpectedRecordCount(
                                                controlFile.toString()
                                        )
                );

        assertEquals(
                true,
                exception.getMessage()
                        .contains(
                                "non-negative integer"
                        )
        );
    }

    @Test
    void shouldRejectNegativeRecordCount()
            throws IOException {

        Path controlFile =
                createControlFile(
                        "record_count=-1"
                );

        IllegalArgumentException exception =
                assertThrows(
                        IllegalArgumentException.class,
                        () ->
                                controlFileService
                                        .readExpectedRecordCount(
                                                controlFile.toString()
                                        )
                );

        assertEquals(
                true,
                exception.getMessage()
                        .contains(
                                "must not be negative"
                        )
        );
    }

    @Test
    void shouldRejectMissingRecordCount()
            throws IOException {

        Path controlFile =
                createControlFile(
                        "some_other_property=value"
                );

        IllegalArgumentException exception =
                assertThrows(
                        IllegalArgumentException.class,
                        () ->
                                controlFileService
                                        .readExpectedRecordCount(
                                                controlFile.toString()
                                        )
                );

        assertEquals(
                "Control file must contain the "
                        + "record_count property.",
                exception.getMessage()
        );
    }

    @Test
    void shouldRejectBlankRecordCount()
            throws IOException {

        Path controlFile =
                createControlFile(
                        "record_count="
                );

        IllegalArgumentException exception =
                assertThrows(
                        IllegalArgumentException.class,
                        () ->
                                controlFileService
                                        .readExpectedRecordCount(
                                                controlFile.toString()
                                        )
                );

        assertEquals(
                "Control file must contain the "
                        + "record_count property.",
                exception.getMessage()
        );
    }

    @Test
    void shouldRejectNonNumericRecordCount()
            throws IOException {

        Path controlFile =
                createControlFile(
                        "record_count=abc"
                );

        IllegalArgumentException exception =
                assertThrows(
                        IllegalArgumentException.class,
                        () ->
                                controlFileService
                                        .readExpectedRecordCount(
                                                controlFile.toString()
                                        )
                );

        assertEquals(
                true,
                exception.getMessage()
                        .contains(
                                "non-negative integer"
                        )
        );
    }

    @Test
    void shouldRejectMissingControlFile() {

        Path missingFile =
                controlDirectory.resolve(
                        "missing.properties"
                );

        IllegalArgumentException exception =
                assertThrows(
                        IllegalArgumentException.class,
                        () ->
                                controlFileService
                                        .readExpectedRecordCount(
                                                missingFile.toString()
                                        )
                );

        assertEquals(
                true,
                exception.getMessage()
                        .contains(
                                "Control file does not exist"
                        )
        );
    }

    @Test
    void shouldRejectControlFileOutsideDataDirectory()
            throws IOException {

        Path outsideFile =
                temporaryDirectory
                        .getParent()
                        .resolve(
                                "outside-control.properties"
                        );

        Files.writeString(
                outsideFile,
                "record_count=10000"
        );

        try {

            IllegalArgumentException exception =
                    assertThrows(
                            IllegalArgumentException.class,
                            () ->
                                    controlFileService
                                            .readExpectedRecordCount(
                                                    outsideFile.toString()
                                            )
                    );

            assertEquals(
                    true,
                    exception.getMessage()
                            .contains(
                                    "control_file_path must be inside"
                            )
            );

        } finally {

            Files.deleteIfExists(
                    outsideFile
            );
        }
    }

    @Test
    void shouldRejectDirectoryAsControlFile() {

        IllegalArgumentException exception =
                assertThrows(
                        IllegalArgumentException.class,
                        () ->
                                controlFileService
                                        .readExpectedRecordCount(
                                                controlDirectory.toString()
                                        )
                );

        assertEquals(
                true,
                exception.getMessage()
                        .contains(
                                "Control file path is not a "
                                        + "regular file"
                        )
        );
    }

    private Path createControlFile(
            String content) throws IOException {

        Path controlFile =
                controlDirectory.resolve(
                        "employee_ingestion_control.properties"
                );

        Files.writeString(
                controlFile,
                content
        );

        return controlFile;
    }
}

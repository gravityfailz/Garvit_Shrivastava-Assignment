package com.amexlumi.ingestion.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Properties;

@Service
public class ControlFileService {

    private static final String RECORD_COUNT_PROPERTY =
            "record_count";

    private final Path dataDirectory;

    public ControlFileService(
            @Value("${lumi.data-directory:/opt/data}")
            String dataDirectory) {

        this.dataDirectory =
                Path.of(dataDirectory)
                        .toAbsolutePath()
                        .normalize();
    }

    public long readExpectedRecordCount(
            String controlFilePath) {

        validateControlFilePath(controlFilePath);

        Path path =
                Path.of(controlFilePath)
                        .toAbsolutePath()
                        .normalize();

        Properties properties =
                new Properties();

        try (InputStream inputStream =
                     Files.newInputStream(path)) {

            properties.load(inputStream);

        } catch (IOException exception) {

            throw new IllegalStateException(
                    "Unable to read control file: "
                            + controlFilePath,
                    exception
            );
        }

        String recordCountValue =
                properties.getProperty(
                        RECORD_COUNT_PROPERTY
                );

        if (recordCountValue == null
                || recordCountValue.isBlank()) {

            throw new IllegalArgumentException(
                    "Control file must contain the "
                            + "record_count property."
            );
        }

        String trimmedRecordCount =
                recordCountValue.trim();


        long recordCount;

        try {

            recordCount =
                    Long.parseLong(
                            trimmedRecordCount
                    );

        } catch (NumberFormatException exception) {

            throw new IllegalArgumentException(
                    "record_count must be a valid "
                            + "non-negative integer. "
                            + "Received: "
                            + recordCountValue,
                    exception
            );
        }

        if (recordCount < 0) {

            throw new IllegalArgumentException(
                    "record_count must not be negative. "
                            + "Received: "
                            + recordCount
            );
        }

        return recordCount;
    }

    private void validateControlFilePath(
            String controlFilePath) {

        if (controlFilePath == null
                || controlFilePath.isBlank()) {

            throw new IllegalArgumentException(
                    "control_file_path is required."
            );
        }

        Path controlPath =
                Path.of(controlFilePath)
                        .toAbsolutePath()
                        .normalize();

        if (!controlPath.startsWith(
                dataDirectory
        )) {

            throw new IllegalArgumentException(
                    "control_file_path must be inside "
                            + dataDirectory
            );
        }

        if (!Files.exists(controlPath)) {

            throw new IllegalArgumentException(
                    "Control file does not exist: "
                            + controlFilePath
            );
        }

        if (!Files.isRegularFile(controlPath)) {

            throw new IllegalArgumentException(
                    "Control file path is not a regular file: "
                            + controlFilePath
            );
        }
    }
}

package com.amexlumi.ingestion.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.UUID;

@Service
public class FilePreparationService {

    private static final Path DATA_DIRECTORY =
            Path.of("/opt/data");

    private static final String PYSPARK_CONTAINER_IMAGE =
            "amex-lumi-case-study-pyspark-splitter";

    private final ObjectMapper objectMapper;

    private final long splitThresholdBytes;

    private final String dockerNetwork;

    private final String hostProjectDirectory;

    private final String pysparkImage;

    public FilePreparationService(
            ObjectMapper objectMapper,
            @Value("${lumi.split-threshold-bytes:52428800}")
            long splitThresholdBytes,
            @Value("${lumi.docker-network:amex-lumi-case-study_default}")
            String dockerNetwork,
            @Value("${lumi.host-project-dir:}")
            String hostProjectDirectory,
            @Value("${lumi.pyspark-image:" + PYSPARK_CONTAINER_IMAGE + "}")
            String pysparkImage) {

        this.objectMapper = objectMapper;
        this.splitThresholdBytes = splitThresholdBytes;
        this.dockerNetwork = dockerNetwork;
        this.hostProjectDirectory = hostProjectDirectory;
        this.pysparkImage = pysparkImage;
    }


    public List<String> prepareFiles(
            String filePath,
            String executionId) {

        validateFilePath(filePath);

        if (executionId == null
                || executionId.isBlank()) {

            throw new IllegalArgumentException(
                    "execution_id must not be blank."
            );
        }

        Path sourcePath =
                Path.of(filePath)
                        .toAbsolutePath()
                        .normalize();

        long fileSize;

        try {
            fileSize = Files.size(sourcePath);
        } catch (IOException exception) {
            throw new IllegalStateException(
                    "Unable to determine file size: "
                            + filePath,
                    exception
            );
        }

        System.out.println(
                "LUMI API: Source file: " + filePath
        );

        System.out.println(
                "LUMI API: Source file size: "
                        + fileSize
                        + " bytes"
        );

        System.out.println(
                "LUMI API: Split threshold: "
                        + splitThresholdBytes
                        + " bytes"
        );

        if (fileSize <= splitThresholdBytes) {

            System.out.println(
                    "LUMI API: File is at or below threshold. "
                            + "Using original file."
            );

            return List.of(filePath);
        }

        System.out.println(
                "LUMI API: File is above threshold. "
                        + "Starting PySpark splitter."
        );

        return splitLargeFile(
                filePath,
                executionId
        );
    }

    private List<String> splitLargeFile(
            String filePath,
            String executionId) {

        if (hostProjectDirectory == null
                || hostProjectDirectory.isBlank()) {

            throw new IllegalStateException(
                    "LUMI_HOST_PROJECT_DIR is not configured."
            );
        }

        Path outputDirectory =
                DATA_DIRECTORY
                        .resolve("split-output")
                        .resolve(executionId)
                        .normalize();

        try {
            Files.createDirectories(outputDirectory);
        } catch (IOException exception) {
            throw new IllegalStateException(
                    "Unable to create split output directory: "
                            + outputDirectory,
                    exception
            );
        }

        String containerOutputDirectory =
                outputDirectory.toString();

        List<String> command =
                buildDockerCommand(
                        filePath,
                        containerOutputDirectory
                );

        System.out.println(
                "LUMI API: Starting PySpark Docker worker."
        );

        System.out.println(
                "LUMI API: PySpark image: "
                        + pysparkImage
        );

        Process process = null;

        try {

            process =
                    new ProcessBuilder(command)
                            .redirectErrorStream(true)
                            .start();

            List<String> outputLines =
                    new ArrayList<>();

            try (BufferedReader reader =
                         new BufferedReader(
                                 new InputStreamReader(
                                         process.getInputStream(),
                                         StandardCharsets.UTF_8
                                 ))) {

                String line;

                while ((line = reader.readLine()) != null) {

                    outputLines.add(line);

                    System.out.println(
                            "PySpark: " + line
                    );
                }
            }

            int exitCode =
                    process.waitFor();

            if (exitCode != 0) {

                throw new IllegalStateException(
                        "PySpark splitter failed with exit code "
                                + exitCode
                                + ". Output: "
                                + String.join(
                                        " | ",
                                        outputLines
                                )
                );
            }

        } catch (IOException exception) {

            throw new IllegalStateException(
                    "Unable to start PySpark Docker worker.",
                    exception
            );

        } catch (InterruptedException exception) {

            Thread.currentThread().interrupt();

            throw new IllegalStateException(
                    "PySpark splitter execution was interrupted.",
                    exception
            );
        }

        Path manifestPath =
                outputDirectory.resolve(
                        "manifest.json"
                );

        if (!Files.exists(manifestPath)) {

            throw new IllegalStateException(
                    "PySpark splitter completed but manifest.json "
                            + "was not created: "
                            + manifestPath
            );
        }

        return readPartPaths(
                manifestPath
        );
    }

    private List<String> buildDockerCommand(
            String filePath,
            String outputDirectory) {

        String hostDataDirectory =
                hostProjectDirectory
                        + "/data";

        return List.of(
                "docker",
                "run",
                "--rm",
                "--network",
                dockerNetwork,
                "--volume",
                hostDataDirectory
                        + ":/opt/data",
                pysparkImage,
                "--input_path",
                filePath,
                "--output_dir",
                outputDirectory,
                "--threshold_bytes",
                String.valueOf(
                        splitThresholdBytes
                )
        );
    }

    private List<String> readPartPaths(
            Path manifestPath) {

        try {

            JsonNode manifest =
                    objectMapper.readTree(
                            manifestPath.toFile()
                    );

            JsonNode parts =
                    manifest.get("parts");

            if (parts == null
                    || !parts.isArray()
                    || parts.isEmpty()) {

                throw new IllegalStateException(
                        "PySpark manifest does not contain "
                                + "any output parts: "
                                + manifestPath
                );
            }

            List<String> filePaths =
                    new ArrayList<>();

            for (JsonNode part : parts) {

                JsonNode filePathNode =
                        part.get("file_path");

                if (filePathNode == null
                        || filePathNode.asText().isBlank()) {

                    throw new IllegalStateException(
                            "PySpark manifest contains a part "
                                    + "without a file_path: "
                                    + manifestPath
                    );
                }

                String partPath =
                        filePathNode.asText();

                Path path =
                        Path.of(partPath)
                                .normalize();

                if (!Files.exists(path)
                        || !Files.isRegularFile(path)) {

                    throw new IllegalStateException(
                            "PySpark output part does not exist: "
                                    + partPath
                    );
                }

                filePaths.add(
                        partPath
                );
            }

            System.out.println(
                    "LUMI API: PySpark generated "
                            + filePaths.size()
                            + " part file(s)."
            );

            for (String filePath : filePaths) {

                System.out.println(
                        "LUMI API: Prepared file: "
                                + filePath
                );
            }

            return filePaths;

        } catch (IOException exception) {

            throw new IllegalStateException(
                    "Unable to read PySpark manifest: "
                            + manifestPath,
                    exception
            );
        }
    }

    private void validateFilePath(
            String filePath) {

        if (filePath == null
                || filePath.isBlank()) {

            throw new IllegalArgumentException(
                    "file_path is required."
            );
        }

        Path sourcePath =
                Path.of(filePath)
                        .toAbsolutePath()
                        .normalize();

        if (!sourcePath.startsWith(
                DATA_DIRECTORY.toAbsolutePath()
        )) {

            throw new IllegalArgumentException(
                    "file_path must be inside "
                            + DATA_DIRECTORY
            );
        }

        if (!Files.exists(sourcePath)) {

            throw new IllegalArgumentException(
                    "Input file does not exist: "
                            + filePath
            );
        }

        if (!Files.isRegularFile(sourcePath)) {

            throw new IllegalArgumentException(
                    "Input path is not a regular file: "
                            + filePath
            );
        }

        String fileName =
                sourcePath.getFileName()
                        .toString()
                        .toLowerCase(Locale.ROOT);

        if (!fileName.endsWith(".csv")
                && !fileName.endsWith(".json")
                && !fileName.endsWith(".xml")) {

            throw new IllegalArgumentException(
                    "Unsupported file type. "
                            + "Supported formats: CSV, JSON, XML"
            );
        }

        if (splitThresholdBytes <= 0) {

            throw new IllegalStateException(
                    "lumi.split-threshold-bytes must be greater than zero."
            );
        }
    }
}

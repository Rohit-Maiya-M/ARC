package com.arc.service;


import com.arc.dto.*;
import com.arc.entity.RepositoryEntity;
import com.arc.entity.RepositoryStatus;

import com.arc.models.RepositoryFile;
import com.arc.repository.RepositoryRepository;
import com.arc.util.RepositoryFileReader;
import com.arc.util.RepositoryScanner;
import com.arc.util.ZipExtractor;
import com.arc.service.KafkaProducerService;
import com.arc.service.AIServiceClient;
import lombok.RequiredArgsConstructor;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import java.time.LocalDateTime;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
@Service
@RequiredArgsConstructor
public class RepositoryService {

    private final RepositoryRepository repositoryRepository;

    private final KafkaProducerService kafkaProducerService;

    private final AIServiceClient aiServiceClient;

    @Value("${settings.paths.storage_path}")
    private String STORAGE_PATH;

    public RepositoryResponseDto uploadRepository(
            MultipartFile file
    ) throws IOException {

        String repoId =
                UUID.randomUUID().toString();

        Path repoRoot =
                Paths.get(
                        STORAGE_PATH,
                        repoId
                );

        Path uploadedFolder =
                repoRoot.resolve("uploaded");

        Path extractedFolder =
                repoRoot.resolve("extracted");

        Files.createDirectories(
                uploadedFolder
        );

        Files.createDirectories(
                extractedFolder
        );

        Path zipPath =
                uploadedFolder.resolve(
                        file.getOriginalFilename()
                );

        file.transferTo(
                zipPath
        );

        ZipExtractor.extractZip(
                zipPath,
                extractedFolder
        );

        List<Path> scannedFiles =
                RepositoryScanner.scanRepository(
                        extractedFolder
                );

        System.out.println(
                "\n===== SCANNED FILES ====="
        );

        scannedFiles.forEach(
                System.out::println
        );

        String repositoryName =
                RepositoryFileReader.getRepositoryName(
                        file.getOriginalFilename()
                );

        List<RepositoryFile> repositoryFiles =
                scannedFiles.stream()
                        .map(path -> {
                            try {

                                return RepositoryFileReader.readFile(
                                        repoId,
                                        repositoryName,
                                        extractedFolder,
                                        path
                                );

                            } catch (Exception e) {

                                throw new RuntimeException(e);

                            }
                        })
                        .toList();

        System.out.println(
                "\n===== REPOSITORY FILES ====="
        );

        repositoryFiles.forEach(f -> {

            System.out.println(
                    "\nFILE : "
                            + f.getRelativePath()
            );

            System.out.println(
                    "EXTENSION : "
                            + f.getExtension()
            );

            System.out.println(
                    "CONTENT LENGTH : "
                            + f.getContent().length()
            );

        });

        RepositoryEntity repositoryEntity =
                RepositoryEntity.builder()
                        .repositoryUuid(
                                repoId
                        )
                        .repositoryName(
                                repositoryName
                        )
                        .originalFileName(
                                file.getOriginalFilename()
                        )
                        .extractedPath(
                                extractedFolder.toString()
                        )
                        .status(
                                RepositoryStatus.UPLOADED
                        )
                        .uploadedAt(
                                LocalDateTime.now()
                        )
                        .build();

        RepositoryEntity savedRepository =
                repositoryRepository.save(
                        repositoryEntity
                );

        System.out.println(
                "\n===== PUBLISHING TO KAFKA ====="
        );

        repositoryFiles.forEach(f -> {

            try {

                kafkaProducerService.publishRepositoryFile(
                        f
                );

            } catch (Exception e) {

                e.printStackTrace();

            }

        });

        return RepositoryResponseDto
                .builder()
                .id(savedRepository.getId())
                .repositoryUuid(savedRepository.getRepositoryUuid())
                .name(savedRepository.getRepositoryName())
                .status(savedRepository.getStatus())
                .uploadedAt(savedRepository.getUploadedAt())
                .build();
    }

    public SummaryResponseDto summarizeRepository(
            Long repositoryId
    ) {

        repositoryRepository.findById(
                        repositoryId
                )
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Repository not found: "
                                        + repositoryId
                        )
                );

        return aiServiceClient.summarizeRepository(
                repositoryId
        );
    }

    public AskResponseDto askRepository(
            Long repositoryId,
            String question
    ) {

        RepositoryEntity repository =
                repositoryRepository.findById(
                        repositoryId
                ).orElseThrow(() ->
                        new IllegalArgumentException(
                                "Repository not found: "
                                        + repositoryId
                        )
                );

        return aiServiceClient.askRepository(
                repository.getRepositoryUuid(),
                question
        );
    }


    public AskResponseDto askGenerativeAIRepository(
            Long repositoryId,
            String question
    ) {

        RepositoryEntity repository =
                repositoryRepository.findById(
                        repositoryId
                ).orElseThrow(() ->
                        new IllegalArgumentException(
                                "Repository not found: "
                                        + repositoryId
                        )
                );

        return aiServiceClient.askGenerativeAIRepository(
                repository.getRepositoryUuid(),
                question
        );
    }

    public Map<String, String> getRepositoryFilesMap(
            Long repositoryId
    ) throws IOException {

        RepositoryEntity repo =
                repositoryRepository.findById(
                                repositoryId
                        )
                        .orElseThrow(() ->
                                new IllegalArgumentException(
                                        "Repository not found"
                                )
                        );

        Path extractedRoot =
                Paths.get(
                        repo.getExtractedPath()
                );

        List<Path> scannedPaths =
                RepositoryScanner.scanRepository(
                        extractedRoot
                );

        Map<String, String> filesMap =
                new java.util.HashMap<>();

        for (Path relPath : scannedPaths) {

            Path fullPath =
                    extractedRoot.resolve(
                            relPath
                    );

            String content =
                    Files.readString(
                            fullPath
                    );

            String cleanKey =
                    "/"
                            + relPath.toString()
                            .replace("\\", "/");

            filesMap.put(
                    cleanKey,
                    content
            );
        }

        return filesMap;
    }

    public List<RepositoryResponseDto> getAllRepository() {

        return repositoryRepository.findAll()
                .stream()
                .map(this::mapToResponse)
                .toList();
    }

    public RepositoryResponseDto getRepository(
            Long repositoryId
    ) {

        RepositoryEntity repository =
                repositoryRepository.findById(
                                repositoryId
                        )
                        .orElseThrow(() ->
                                new IllegalArgumentException(
                                        "Repository not found: "
                                                + repositoryId
                                )
                        );

        return mapToResponse(
                repository
        );
    }

    private RepositoryResponseDto mapToResponse(RepositoryEntity repo){
        return RepositoryResponseDto.builder()
                .id(repo.getId())
                .repositoryUuid(repo.getRepositoryUuid())
                .name(repo.getRepositoryName())
                .status(repo.getStatus())
                .uploadedAt(repo.getUploadedAt())
                .build();
    }
}
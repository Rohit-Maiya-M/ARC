package com.arc.service;

import com.arc.chunking.SemanticChunker;
import com.arc.dto.IndexRequestDto;
import com.arc.dto.RepositoryResponseDto;
import com.arc.dto.SummaryResponseDto;
import com.arc.entity.RepositoryEntity;
import com.arc.entity.RepositoryStatus;
import com.arc.models.CodeChunk;
import com.arc.models.RepositoryFile;
import com.arc.repository.RepositoryRepository;
import com.arc.util.RepositoryFileReader;
import com.arc.util.RepositoryScanner;
import com.arc.util.ZipExtractor;

import lombok.RequiredArgsConstructor;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import java.time.LocalDateTime;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class RepositoryService {

    private final RepositoryRepository repositoryRepository;
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

        Files.createDirectories(uploadedFolder);

        Files.createDirectories(extractedFolder);

        Path zipPath =
                uploadedFolder.resolve(
                        file.getOriginalFilename()
                );

        file.transferTo(zipPath);

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

        scannedFiles.forEach(System.out::println);

        List<RepositoryFile> repositoryFiles =
                scannedFiles.stream()
                        .map(path -> {
                            try {
                                return RepositoryFileReader
                                        .readFile(
                                                extractedFolder,
                                                path
                                        );
                            }
                            catch (Exception e) {
                                throw new RuntimeException(e);
                            }
                        })
                        .toList();

        System.out.println(
                "\n===== REPOSITORY FILES ====="
        );

        repositoryFiles.forEach(f -> {

            System.out.println(
                    "\nFILE: "
                            + f.getRelativePath()
            );

            System.out.println(
                    "EXTENSION: "
                            + f.getExtension()
            );

            System.out.println(
                    "CONTENT LENGTH: "
                            + f.getContent().length()
            );
        });

        /*
         * SAVE REPOSITORY FIRST
         */

        RepositoryEntity repositoryEntity =
                RepositoryEntity.builder()
                        .name(
                                file.getOriginalFilename()
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

        /*
         * CHUNKING
         */

        List<CodeChunk> codeChunks =
                repositoryFiles.stream()
                        .flatMap(f ->
                                SemanticChunker
                                        .chunkRepositoryFile(f)
                                        .stream()
                        )
                        .toList();

        System.out.println(
                "\n===== CODE CHUNKS ====="
        );

        codeChunks.forEach(chunk -> {

            System.out.println(
                    "\nCHUNK ID: "
                            + chunk.getChunkId()
            );

            System.out.println(
                    "FILE: "
                            + chunk.getRelativePath()
            );

            System.out.println(
                    "CONTENT LENGTH: "
                            + chunk.getContent().length()
            );

            IndexRequestDto request =
                    IndexRequestDto.builder()

                            .chunkId(
                                    chunk.getChunkId()
                            )

                            .repositoryId(
                                    savedRepository.getId()
                            )

                            .content(
                                    chunk.getContent()
                            )

                            .metadata(
                                    Map.of(
                                            "filename",
                                            chunk.getFileName(),

                                            "extension",
                                            chunk.getExtension(),

                                            "content",
                                            chunk.getContent()
                                    )
                            )

                            .build();

            aiServiceClient.indexChunk(
                    request
            );
        });

        return RepositoryResponseDto
                .builder()
                .id(
                        savedRepository.getId()
                )
                .name(
                        savedRepository.getName()
                )
                .status(
                        savedRepository.getStatus()
                )
                .uploadedAt(
                        savedRepository.getUploadedAt()
                )
                .build();
    }

    public SummaryResponseDto summarizeRepository(
            Long repositoryId
    ) {
        repositoryRepository.findById(repositoryId)
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
}

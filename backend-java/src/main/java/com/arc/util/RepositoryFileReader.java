package com.arc.util;

import com.arc.models.RepositoryFile;

import java.io.IOException;

import java.nio.file.Files;
import java.nio.file.Path;

import java.util.UUID;

public class RepositoryFileReader {

    public static RepositoryFile readFile(
            String repositoryId,
            String repositoryName,
            Path rootPath,
            Path filePath
    ) throws IOException {

        String content =
                Files.readString(
                        filePath
                );

        String fileName =
                filePath.getFileName()
                        .toString();

        String extension =
                getExtension(
                        fileName
                );

        String relativePath =
                rootPath
                        .relativize(filePath)
                        .toString()
                        .replace("\\", "/");

        return RepositoryFile.builder()
                .repositoryUuid(
                        repositoryId
                )
                .repositoryName(
                        repositoryName
                )
                .fileId(
                        UUID.randomUUID().toString()
                )
                .fileName(
                        fileName
                )
                .relativePath(
                        relativePath
                )
                .extension(
                        extension
                )
                .content(
                        content
                )
                .build();
    }

    private static String getExtension(
            String fileName
    ) {

        int lastDot =
                fileName.lastIndexOf('.');

        if (lastDot == -1) {
            return "";
        }

        return fileName.substring(lastDot);
    }

    public static String getRepositoryName(
            String filename
    ) {

        if (filename == null) {
            return null;
        }

        int dotIndex =
                filename.lastIndexOf('.');

        int separatorIndex =
                Math.max(
                        filename.lastIndexOf('/'),
                        filename.lastIndexOf('\\')
                );

        if (dotIndex > separatorIndex) {

            return filename.substring(
                    0,
                    dotIndex
            );
        }

        return filename;
    }
}
package com.arc.util;

import com.arc.models.RepositoryFile;

import java.io.IOException;

import java.nio.file.Files;
import java.nio.file.Path;

public class RepositoryFileReader {

    public static RepositoryFile readFile(
            Path rootPath,
            Path filePath
    ) throws IOException {

        String content =
                Files.readString(filePath);

        String fileName =
                filePath.getFileName()
                        .toString();

        String extension =
                getExtension(fileName);

        String relativePath =
                rootPath
                        .relativize(filePath)
                        .toString();

        return RepositoryFile
                .builder()
                .fileName(fileName)
                .relativePath(relativePath)
                .extension(extension)
                .content(content)
                .build();
    }

    private static String getExtension(
            String fileName
    ) {

        int lastDot =
                fileName.lastIndexOf(".");

        if (lastDot == -1) {

            return "";
        }

        return fileName.substring(lastDot + 1);
    }
}
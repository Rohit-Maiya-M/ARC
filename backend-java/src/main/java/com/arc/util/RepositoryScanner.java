package com.arc.util;

import java.io.IOException;

import java.nio.file.Files;
import java.nio.file.Path;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.stream.Stream;

public class RepositoryScanner {

    private static final Set<String>
            SUPPORTED_EXTENSIONS = Set.of(

            ".java",
            ".js",
            ".jsx",
            ".ts",
            ".tsx",
            ".py",
            ".json",
            ".yml",
            ".yaml",
            ".sql"
    );

    private static final Set<String>
            IGNORED_DIRECTORIES = Set.of(

            "node_modules",
            "target",
            "build",
            "dist",
            ".git",
            ".idea",
            ".venv"
    );

    public static List<Path> scanRepository(
            Path repositoryPath
    ) throws IOException {

        List<Path> sourceFiles =
                new ArrayList<>();

        try (
                Stream<Path> paths =
                        Files.walk(repositoryPath)
        ) {

            paths.forEach(path -> {

                try {

                    if (
                            Files.isDirectory(path)
                    ) {

                        String dirName =
                                path.getFileName()
                                        .toString();

                        if (
                                IGNORED_DIRECTORIES
                                        .contains(dirName)
                        ) {

                            return;
                        }
                    }

                    if (
                            Files.isRegularFile(path)
                    ) {

                        String fileName =
                                path.getFileName()
                                        .toString();

                        if (
                                isSupportedFile(fileName)
                        ) {

                            sourceFiles.add(path);
                        }
                    }

                } catch (Exception e) {

                    e.printStackTrace();
                }
            });
        }

        return sourceFiles;
    }

    private static boolean isSupportedFile(
            String fileName
    ) {

        return SUPPORTED_EXTENSIONS
                .stream()
                .anyMatch(fileName::endsWith)

                ||

                fileName.equals("pom.xml")

                ||

                fileName.equals("build.gradle");
    }
}
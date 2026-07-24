package com.arc.chunking;

import com.arc.models.CodeChunk;
import com.arc.models.RepositoryFile;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

public class SemanticChunker {

    private static final int CHUNK_SIZE = 150;
    
    private static final int OVERLAP = 30;

    public static List<CodeChunk> chunkRepositoryFile(
            RepositoryFile repositoryFile
    ) {

        String content = repositoryFile.getContent();

        if (content == null || content.isBlank()) {
            return List.of();
        }

        String[] words = content
                .trim()
                .split("\\s+");

        List<CodeChunk> chunks = new ArrayList<>();

        int step = CHUNK_SIZE - OVERLAP;

        for (int start = 0; start < words.length; start += step) {

            int end = Math.min(start + CHUNK_SIZE, words.length);

            if (end <= start) {
                break;
            }

            String chunkContent = String.join(
                    " ",
                    Arrays.copyOfRange(words, start, end)
            ).trim();

            if (chunkContent.isBlank()) {
                continue;
            }

            CodeChunk chunk = CodeChunk.builder()
                    .chunkId(UUID.randomUUID().toString())
                    .fileName(repositoryFile.getFileName())
                    .relativePath(repositoryFile.getRelativePath())
                    .extension(repositoryFile.getExtension())
                    .content(chunkContent)
                    .build();

            chunks.add(chunk);

            if (end == words.length) {
                break;
            }
        }

        return chunks;
    }

}
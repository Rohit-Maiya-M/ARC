package com.arc.chunking;

import com.arc.models.CodeChunk;
import com.arc.models.RepositoryFile;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

public class SemanticChunker {

    public static List<CodeChunk> chunkRepositoryFile(
            RepositoryFile repositoryFile
    ){

        String content = repositoryFile.getContent();
        int chunkSize = 500;
        int overlap = 100;

        List<CodeChunk> chunks = new ArrayList<>();
        String[] words = content.split("\\s+");

        for(int start=0; start < words.length; start += (chunkSize - overlap)){
            int end = Math.min(start + chunkSize, words.length);
            String chunkContent = String.join(" ", Arrays.copyOfRange(words, start, end));

            CodeChunk chunk = CodeChunk.builder()
                    .chunkId(UUID.randomUUID().toString())
                    .fileName(repositoryFile.getFileName())
                    .relativePath(repositoryFile.getRelativePath())
                    .extension(repositoryFile.getExtension())
                    .content(chunkContent)
                    .build();

            chunks.add(chunk);
        }
        
        return chunks;

    }

}

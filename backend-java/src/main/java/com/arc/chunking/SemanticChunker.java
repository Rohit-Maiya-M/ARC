package com.arc.chunking;

import com.arc.models.CodeChunk;
import com.arc.models.RepositoryFile;

import java.util.List;
import java.util.UUID;

public class SemanticChunker {

    public static List<CodeChunk> chunkRepositoryFile(
            RepositoryFile repositoryFile
    ){
        CodeChunk chunk = CodeChunk.builder()
                .chunkId(UUID.randomUUID().toString())
                .fileName(repositoryFile.getFileName())
                .relativePath(repositoryFile.getRelativePath())
                .extension(repositoryFile.getExtension())
                .content(repositoryFile.getContent())
                .build();

        return List.of(chunk);
    }
}

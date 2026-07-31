package com.arc.models;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class RepositoryFile {

    @JsonProperty("repository_id")
    private String repositoryUuid;

    @JsonProperty("repository_name")
    private String repositoryName;

    @JsonProperty("file_id")
    private String fileId;

    @JsonProperty("file_name")
    private String fileName;

    @JsonProperty("relative_path")
    private String relativePath;

    @JsonProperty("extension")
    private String extension;

    @JsonProperty("content")
    private String content;
}
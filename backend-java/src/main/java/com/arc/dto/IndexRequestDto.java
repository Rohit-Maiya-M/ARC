package com.arc.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Map;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class IndexRequestDto {

    @JsonProperty("chunk_id")
    private String chunkId;

    @JsonProperty("repository_id")
    private Long repositoryId;

    private String content;

    private Map<String, String> metadata;
}
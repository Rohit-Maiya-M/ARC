package com.arc.dto;

import com.arc.entity.RepositoryStatus;
import lombok.Builder;
import lombok.Data;


import java.time.LocalDateTime;

@Data
@Builder
public class RepositoryResponseDto {

    private Long id;

    private String repositoryUuid;

    private String name;

    private RepositoryStatus status;

    private LocalDateTime uploadedAt;
}
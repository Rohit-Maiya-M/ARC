package com.arc.entity;


import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Data
@Table(name = "repositories")
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RepositoryEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;


    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String originalFileName;

    @Column(nullable = false)
    private String extractedPath;

    @Enumerated(EnumType.STRING)
    private RepositoryStatus status;

    @Column(nullable = false)
    private LocalDateTime uploadedAt;

}

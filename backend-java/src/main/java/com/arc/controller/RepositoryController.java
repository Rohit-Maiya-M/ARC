package com.arc.controller;

import com.arc.dto.RepositoryResponseDto;
import com.arc.dto.SummaryResponseDto;
import com.arc.service.RepositoryService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

@RestController
@RequestMapping("/repositories")
@RequiredArgsConstructor
public class RepositoryController {

    private final RepositoryService repositoryService;

    @PostMapping("/upload")
    public ResponseEntity<RepositoryResponseDto>
    uploadRepository(

            @RequestParam("file")
            MultipartFile file

    ) throws IOException {

        RepositoryResponseDto response =
                repositoryService
                        .uploadRepository(file);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(response);
    }

    @PostMapping("/{repositoryId}/summary")
    public ResponseEntity<SummaryResponseDto>
    summarizeRepository(

            @PathVariable
            Long repositoryId

    ) {

        SummaryResponseDto response =
                repositoryService
                        .summarizeRepository(repositoryId);

        return ResponseEntity
                .ok(response);
    }
}

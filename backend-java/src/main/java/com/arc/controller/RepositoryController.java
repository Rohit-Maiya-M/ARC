package com.arc.controller;

import com.arc.dto.*;
import com.arc.service.RepositoryService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/repositories")
@RequiredArgsConstructor
@CrossOrigin(origins = "http://localhost:3000")
public class RepositoryController {

    private final RepositoryService repositoryService;

    @GetMapping
    public ResponseEntity<List<RepositoryResponseDto>> getAllRepository(){
        List<RepositoryResponseDto> response = repositoryService.getAllRepository();

        return ResponseEntity.ok(response);
    }

    @GetMapping("/{repositoryId}")
    public ResponseEntity<RepositoryResponseDto> getRepository(
            @PathVariable
            Long repositoryId
    ){
        RepositoryResponseDto response = repositoryService.getRepository(repositoryId);

        return ResponseEntity.ok(response);
    }

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


    @PostMapping("/{repositoryId}/ask")
    public ResponseEntity<AskResponseDto> askRepository(
            @PathVariable Long repositoryId,
            @Valid @RequestBody AskQuestionRequestDTO dto
    ) {

        AskResponseDto response =
                repositoryService.askRepository(
                        repositoryId,
                        dto.getQuestion()
                );

        return ResponseEntity.ok(response);
    }

    @PostMapping("/{repositoryId}/gemini/ask")
    public ResponseEntity<AskResponseDto> askGenerativeAIRepository(
            @PathVariable Long repositoryId,
            @Valid @RequestBody AskQuestionRequestDTO dto
    ){
        AskResponseDto response = repositoryService.askGenerativeAIRepository(
                repositoryId,
                dto.getQuestion()
        );

        return ResponseEntity.ok(response);
    }

    @GetMapping("/{repositoryId}/files")
    public ResponseEntity<Map<String, String>> getRepositoryFiles(@PathVariable Long repositoryId) throws IOException {
        Map<String, String> files = repositoryService.getRepositoryFilesMap(repositoryId);
        return ResponseEntity.ok(files);
    }

}

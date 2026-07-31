package com.arc.service;

import com.arc.dto.*;
import com.arc.models.RepositoryFile;

import lombok.RequiredArgsConstructor;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
@RequiredArgsConstructor
public class AIServiceClient {

    private final RestTemplate restTemplate;
    private final KafkaProducerService producerService;

    @Value("${settings.paths.index_url}")
    private String indexUrl;

    @Value("${settings.paths.summary_url}")
    private String summaryUrl;

    @Value("${settings.paths.ask_url}")
    private String askUrl;

    @Value("${settings.paths.ask_generative_ai_url}")
    private String askGenerativeAIUrl;


    public void indexFile(
            RepositoryFile repositoryFile
    ) {

        producerService.publishRepositoryFile(
                repositoryFile
        );
    }


    public SummaryResponseDto summarizeRepository(
            Long repositoryId
    ) {

        SummaryRequestDto request =
                SummaryRequestDto.builder()
                        .repositoryId(repositoryId)
                        .build();

        return restTemplate.postForObject(
                summaryUrl,
                request,
                SummaryResponseDto.class
        );
    }


    public AskResponseDto askRepository(
            String repositoryUuid,
            String question
    ) {

        AskRequestDto request =
                AskRequestDto.builder()
                        .repositoryId(repositoryUuid)
                        .question(question)
                        .build();

        return restTemplate.postForObject(
                askUrl,
                request,
                AskResponseDto.class
        );
    }


    public AskResponseDto askGenerativeAIRepository(
            String repositoryUuid,
            String question
    ) {

        AskRequestDto request =
                AskRequestDto.builder()
                        .repositoryId(repositoryUuid)
                        .question(question)
                        .build();

        return restTemplate.postForObject(
                askGenerativeAIUrl,
                request,
                AskResponseDto.class
        );
    }
}
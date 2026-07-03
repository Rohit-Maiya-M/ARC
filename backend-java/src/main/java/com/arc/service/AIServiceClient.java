package com.arc.service;


import com.arc.dto.*;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import tools.jackson.databind.ObjectMapper;

@Service
@RequiredArgsConstructor
public class AIServiceClient {

    private final RestTemplate restTemplate;
    private final KafkaProducerService producerService;
    private final ObjectMapper objectMapper;

    @Value("${settings.paths.index_url}")
    private String indexUrl;

    @Value("${settings.paths.summary_url}")
    private String summaryUrl;

    @Value("${settings.paths.ask_url}")
    private String askUrl;

    @Value("${settings.paths.ask_generative_ai_url}")
    private String askGenerativeAIUrl;

    public void indexChunk(IndexBatchRequestDTO requests) {
        try {
            String jsonBatch = objectMapper.writeValueAsString(requests);
            producerService.sendBatch(jsonBatch);
        } catch (Exception e) {
            throw new RuntimeException("Failed to index batch", e);
        }
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
            Long repositoryId,
            String question
    ){
        AskRequestDto request =
                AskRequestDto.builder()
                        .repositoryId(repositoryId)
                        .question(question)
                        .build();

        return restTemplate.postForObject(
                askUrl,
                request,
                AskResponseDto.class
        );
    }

    public AskResponseDto askGenerativeAIRepository(
            Long repositoryId,
            String question
    ){
        AskRequestDto request = AskRequestDto.builder()
                .repositoryId(repositoryId)
                .question(question)
                .build();

        return restTemplate.postForObject(
                askGenerativeAIUrl,
                request,
                AskResponseDto.class
        );
    }

}

package com.arc.service;


import com.arc.dto.IndexRequestDto;
import com.arc.dto.SummaryRequestDto;
import com.arc.dto.SummaryResponseDto;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
@RequiredArgsConstructor
public class AIServiceClient {

    private final RestTemplate restTemplate;

    @Value("${settings.paths.index_url}")
    private String indexUrl;

    @Value("${settings.paths.summary_url}")
    private String summaryUrl;

    public void indexChunk(
            IndexRequestDto request
    ) {

        System.out.println(
                "Indexing chunk: "
                        + request.getChunkId()
        );

        restTemplate.postForObject(
                indexUrl,
                request,
                String.class
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
}

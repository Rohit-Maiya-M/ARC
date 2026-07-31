package com.arc.service;

import com.arc.models.RepositoryFile;

import lombok.RequiredArgsConstructor;

import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import tools.jackson.databind.ObjectMapper;

@Service
@RequiredArgsConstructor
public class KafkaProducerService {

    private static final String TOPIC = "arc.index";

    private final KafkaTemplate<String, String> kafkaTemplate;

    private final ObjectMapper objectMapper;

    public void publishRepositoryFile(
            RepositoryFile repositoryFile
    ) {

        try {

            String json = objectMapper.writeValueAsString(
                    repositoryFile
            );

            kafkaTemplate
                    .send(
                            TOPIC,
                            json
                    )
                    .get();

            System.out.println(
                    "✅ Published : "
                            + repositoryFile.getRelativePath()
            );

        }
        catch (Exception e) {

            throw new RuntimeException(
                    "Failed to publish "
                            + repositoryFile.getRelativePath(),
                    e
            );

        }
    }
}
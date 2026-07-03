package com.arc.service;

import lombok.RequiredArgsConstructor;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class KafkaProducerService {

    private final KafkaTemplate<String, String> kafkaTemplate;

    public void sendBatch(String jsonBatch) {
        kafkaTemplate.send("arc.index", jsonBatch);
        System.out.println("✅ Sent batch to Kafka: " + jsonBatch);
    }
}

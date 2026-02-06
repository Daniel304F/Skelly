package com.example.testmitjav.inbound.messaging;

import com.example.testmitjav.domain.service.ExampleService;
import org.springframework.stereotype.Component;

/**
 * Message Consumer (Inbound Adapter) - Handles incoming messages.
 * Example: RabbitMQ @RabbitListener or Kafka @KafkaListener
 */
@Component
public class ExampleMessageConsumer {

    private final ExampleService exampleService;

    public ExampleMessageConsumer(ExampleService exampleService) {
        this.exampleService = exampleService;
    }

    // @RabbitListener(queues = "example.queue")
    public void handleExampleEvent(String message) {
        // Parse message and delegate to domain service
        System.out.println("Received message: " + message);
    }
}

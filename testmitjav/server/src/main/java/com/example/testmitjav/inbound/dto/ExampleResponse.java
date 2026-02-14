package com.example.testmitjav.inbound.dto;

import com.example.testmitjav.domain.model.Example;
import java.util.UUID;

/**
 * Response DTO - Data transfer object for outgoing responses.
 */
public record ExampleResponse(
    UUID id,
    String name,
    String description
) {
    public static ExampleResponse from(Example example) {
        return new ExampleResponse(
            example.getId(),
            example.getName(),
            example.getDescription()
        );
    }
}

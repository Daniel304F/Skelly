package com.example.testmitjav.domain.model;

import java.util.UUID;

/**
 * Domain Entity - Core business object.
 * Contains business logic and is independent of infrastructure.
 */
public class Example {

    private final UUID id;
    private String name;
    private String description;

    public Example(UUID id, String name, String description) {
        this.id = id;
        this.name = name;
        this.description = description;
    }

    public static Example create(String name, String description) {
        return new Example(UUID.randomUUID(), name, description);
    }

    // Getters
    public UUID getId() { return id; }
    public String getName() { return name; }
    public String getDescription() { return description; }

    // Business methods
    public void updateDetails(String name, String description) {
        this.name = name;
        this.description = description;
    }
}

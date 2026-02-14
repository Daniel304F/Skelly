package com.example.testmitjav.outbound.restclient;

import com.example.testmitjav.domain.client.ExternalServiceClient;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.Optional;

/**
 * REST Client Implementation (Outbound Adapter) - Calls external web services.
 * Implements the domain client interface.
 */
@Component
public class ExternalServiceClientImpl implements ExternalServiceClient {

    private final RestTemplate restTemplate;
    private static final String EXTERNAL_SERVICE_URL = "https://api.example.com";

    public ExternalServiceClientImpl() {
        this.restTemplate = new RestTemplate();
    }

    @Override
    public Optional<String> fetchExternalData(String resourceId) {
        try {
            String url = EXTERNAL_SERVICE_URL + "/resources/" + resourceId;
            String response = restTemplate.getForObject(url, String.class);
            return Optional.ofNullable(response);
        } catch (Exception e) {
            return Optional.empty();
        }
    }

    @Override
    public void notifyExternalService(String eventType, String payload) {
        try {
            String url = EXTERNAL_SERVICE_URL + "/events";
            restTemplate.postForEntity(url, payload, Void.class);
        } catch (Exception e) {
            System.err.println("Failed to notify external service: " + e.getMessage());
        }
    }
}

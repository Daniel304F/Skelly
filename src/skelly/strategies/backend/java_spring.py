import subprocess
from typing import List
from pathlib import Path

from skelly.strategies.base import BackendStrategy
from skelly.core.models import ProjectConfig


class JavaSpringBackend(BackendStrategy):
    """Java Spring Boot backend with Maven."""

    def __init__(self, project_name: str):
        self.project_name = project_name.lower().replace(" ", "")
        self.base_package = f"com.example.{self.project_name}"

    def get_folders(self) -> List[str]:
        return ["server/src/main/resources"]

    def get_name(self) -> str:
        return "Java Spring Boot"

    DEPENDENCY_MAP = {
        "spring-boot-starter-security": ("org.springframework.boot", None),
        "spring-boot-starter-data-jpa": ("org.springframework.boot", None),
        "spring-boot-starter-actuator": ("org.springframework.boot", None),
        "lombok": ("org.projectlombok", "1.18.30"),
        "mapstruct": ("org.mapstruct", "1.5.5.Final"),
    }

    def create_config_files(self, config: ProjectConfig, base_path: Path) -> None:
        dependencies_xml = ""

        for lib in config.backend_libraries:
            dep_info = self.DEPENDENCY_MAP.get(lib)
            if dep_info:
                group_id, version = dep_info
            else:
                group_id = "org.springframework.boot"
                version = None

            if version:
                dependencies_xml += f"""
        <dependency>
            <groupId>{group_id}</groupId>
            <artifactId>{lib}</artifactId>
            <version>{version}</version>
        </dependency>"""
            else:
                dependencies_xml += f"""
        <dependency>
            <groupId>{group_id}</groupId>
            <artifactId>{lib}</artifactId>
        </dependency>"""

        pom_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>{self.project_name}</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    <packaging>jar</packaging>

    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
        <relativePath/>
    </parent>

    <properties>
        <java.version>17</java.version>
    </properties>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>{dependencies_xml}
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
"""
        server_path = base_path / "server"
        pom_path = server_path / "pom.xml"
        with open(pom_path, "w") as f:
            f.write(pom_content.strip())

        print("[cyan]Created server/pom.xml[/cyan]")

        if config.architecture == "Hexagonal Architecture":
            self._generate_hexagonal_example(config, base_path)

    def _generate_hexagonal_example(self, config: ProjectConfig, base_path: Path) -> None:
        """Generate example code with inbound/domain/outbound structure."""
        pkg = self.base_package
        pkg_path = f"server/src/main/java/{pkg.replace('.', '/')}"

        print("[cyan]Generating hexagonal architecture example (inbound/domain/outbound)...[/cyan]")

        # ╔═══════════════════════════════════════════════════════════════╗
        # ║                     DOMAIN LAYER                              ║
        # ╚═══════════════════════════════════════════════════════════════╝

        # Domain Model: Entity
        entity_code = f'''package {pkg}.domain.model;

import java.util.UUID;

/**
 * Domain Entity - Core business object.
 * Contains business logic and is independent of infrastructure.
 */
public class Example {{

    private final UUID id;
    private String name;
    private String description;

    public Example(UUID id, String name, String description) {{
        this.id = id;
        this.name = name;
        this.description = description;
    }}

    public static Example create(String name, String description) {{
        return new Example(UUID.randomUUID(), name, description);
    }}

    // Getters
    public UUID getId() {{ return id; }}
    public String getName() {{ return name; }}
    public String getDescription() {{ return description; }}

    // Business methods
    public void updateDetails(String name, String description) {{
        this.name = name;
        this.description = description;
    }}
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/domain/model/Example.java", entity_code)

        # Domain Service
        domain_service_code = f'''package {pkg}.domain.service;

import {pkg}.domain.model.Example;
import {pkg}.domain.repository.ExampleRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Domain Service - Contains business logic.
 * Uses repository interfaces (ports) for data access.
 */
@Service
public class ExampleService {{

    private final ExampleRepository exampleRepository;

    public ExampleService(ExampleRepository exampleRepository) {{
        this.exampleRepository = exampleRepository;
    }}

    public Example createExample(String name, String description) {{
        Example example = Example.create(name, description);
        return exampleRepository.save(example);
    }}

    public Optional<Example> findById(UUID id) {{
        return exampleRepository.findById(id);
    }}

    public List<Example> findAll() {{
        return exampleRepository.findAll();
    }}

    public void deleteById(UUID id) {{
        exampleRepository.deleteById(id);
    }}
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/domain/service/ExampleService.java", domain_service_code)

        # Domain Repository Interface (Port)
        repository_interface_code = f'''package {pkg}.domain.repository;

import {pkg}.domain.model.Example;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

/**
 * Repository Interface (Port) - Defines data access contract.
 * Implementation is in outbound/persistence layer.
 */
public interface ExampleRepository {{

    Example save(Example example);

    Optional<Example> findById(UUID id);

    List<Example> findAll();

    void deleteById(UUID id);
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/domain/repository/ExampleRepository.java", repository_interface_code)

        # Domain Client Interface (Port for external services)
        client_interface_code = f'''package {pkg}.domain.client;

import java.util.Optional;

/**
 * Service Client Interface (Port) - For calling external web services.
 * Implementation is in outbound/restclient layer.
 */
public interface ExternalServiceClient {{

    Optional<String> fetchExternalData(String resourceId);

    void notifyExternalService(String eventType, String payload);
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/domain/client/ExternalServiceClient.java", client_interface_code)

        # Domain MessageProducer Interface (Port)
        message_producer_interface_code = f'''package {pkg}.domain.messaging;

/**
 * Message Producer Interface (Port) - For publishing events.
 * Implementation is in outbound/messaging layer (e.g., RabbitMQ).
 */
public interface ExampleEventProducer {{

    void publishExampleCreated(String exampleId, String name);

    void publishExampleDeleted(String exampleId);
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/domain/messaging/ExampleEventProducer.java", message_producer_interface_code)

        # ╔═══════════════════════════════════════════════════════════════╗
        # ║                    INBOUND LAYER                              ║
        # ╚═══════════════════════════════════════════════════════════════╝

        # Inbound DTO: Request
        request_dto_code = f'''package {pkg}.inbound.dto;

/**
 * Request DTO - Data transfer object for incoming requests.
 */
public record ExampleRequest(
    String name,
    String description
) {{}}
'''
        self._write_java_file(base_path, f"{pkg_path}/inbound/dto/ExampleRequest.java", request_dto_code)

        # Inbound DTO: Response
        response_dto_code = f'''package {pkg}.inbound.dto;

import {pkg}.domain.model.Example;
import java.util.UUID;

/**
 * Response DTO - Data transfer object for outgoing responses.
 */
public record ExampleResponse(
    UUID id,
    String name,
    String description
) {{
    public static ExampleResponse from(Example example) {{
        return new ExampleResponse(
            example.getId(),
            example.getName(),
            example.getDescription()
        );
    }}
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/inbound/dto/ExampleResponse.java", response_dto_code)

        # Inbound REST Controller
        controller_code = f'''package {pkg}.inbound.rest;

import {pkg}.domain.model.Example;
import {pkg}.domain.service.ExampleService;
import {pkg}.inbound.dto.ExampleRequest;
import {pkg}.inbound.dto.ExampleResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

/**
 * REST Controller (Inbound Adapter) - Handles HTTP requests.
 * Converts DTOs to domain objects and delegates to domain service.
 */
@RestController
@RequestMapping("/api/examples")
public class ExampleController {{

    private final ExampleService exampleService;

    public ExampleController(ExampleService exampleService) {{
        this.exampleService = exampleService;
    }}

    @GetMapping
    public ResponseEntity<List<ExampleResponse>> getAll() {{
        List<ExampleResponse> responses = exampleService.findAll()
                .stream()
                .map(ExampleResponse::from)
                .toList();
        return ResponseEntity.ok(responses);
    }}

    @GetMapping("/{{id}}")
    public ResponseEntity<ExampleResponse> getById(@PathVariable UUID id) {{
        return exampleService.findById(id)
                .map(ExampleResponse::from)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }}

    @PostMapping
    public ResponseEntity<ExampleResponse> create(@RequestBody ExampleRequest request) {{
        Example created = exampleService.createExample(
                request.name(),
                request.description()
        );
        return ResponseEntity.ok(ExampleResponse.from(created));
    }}

    @DeleteMapping("/{{id}}")
    public ResponseEntity<Void> delete(@PathVariable UUID id) {{
        exampleService.deleteById(id);
        return ResponseEntity.noContent().build();
    }}
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/inbound/rest/ExampleController.java", controller_code)

        # Inbound Message Consumer (placeholder)
        message_consumer_code = f'''package {pkg}.inbound.messaging;

import {pkg}.domain.service.ExampleService;
import org.springframework.stereotype.Component;

/**
 * Message Consumer (Inbound Adapter) - Handles incoming messages.
 * Example: RabbitMQ @RabbitListener or Kafka @KafkaListener
 */
@Component
public class ExampleMessageConsumer {{

    private final ExampleService exampleService;

    public ExampleMessageConsumer(ExampleService exampleService) {{
        this.exampleService = exampleService;
    }}

    // @RabbitListener(queues = "example.queue")
    public void handleExampleEvent(String message) {{
        // Parse message and delegate to domain service
        System.out.println("Received message: " + message);
    }}
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/inbound/messaging/ExampleMessageConsumer.java", message_consumer_code)

        # Inbound Security Config (placeholder)
        security_config_code = f'''package {pkg}.inbound.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

/**
 * Security Configuration (Inbound) - Configures authentication and authorization.
 * Uncomment and configure when spring-boot-starter-security is added.
 */
// @Configuration
// @EnableWebSecurity
public class SecurityConfig {{

    // @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {{
        http
            .csrf(csrf -> csrf.disable())
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/**").permitAll()
                .anyRequest().authenticated()
            );
        return http.build();
    }}
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/inbound/security/SecurityConfig.java", security_config_code)

        # ╔═══════════════════════════════════════════════════════════════╗
        # ║                   OUTBOUND LAYER                              ║
        # ╚═══════════════════════════════════════════════════════════════╝

        # Outbound Persistence: Repository Implementation
        persistence_impl_code = f'''package {pkg}.outbound.persistence;

import {pkg}.domain.model.Example;
import {pkg}.domain.repository.ExampleRepository;
import org.springframework.stereotype.Repository;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Repository Implementation (Outbound Adapter) - JPA/In-Memory persistence.
 * Implements the domain repository interface.
 */
@Repository
public class ExampleRepositoryImpl implements ExampleRepository {{

    // In-memory storage (replace with JPA Repository in production)
    private final Map<UUID, Example> storage = new ConcurrentHashMap<>();

    @Override
    public Example save(Example example) {{
        storage.put(example.getId(), example);
        return example;
    }}

    @Override
    public Optional<Example> findById(UUID id) {{
        return Optional.ofNullable(storage.get(id));
    }}

    @Override
    public List<Example> findAll() {{
        return new ArrayList<>(storage.values());
    }}

    @Override
    public void deleteById(UUID id) {{
        storage.remove(id);
    }}
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/outbound/persistence/ExampleRepositoryImpl.java", persistence_impl_code)

        # Outbound REST Client: External Service Client Implementation
        rest_client_impl_code = f'''package {pkg}.outbound.restclient;

import {pkg}.domain.client.ExternalServiceClient;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.Optional;

/**
 * REST Client Implementation (Outbound Adapter) - Calls external web services.
 * Implements the domain client interface.
 */
@Component
public class ExternalServiceClientImpl implements ExternalServiceClient {{

    private final RestTemplate restTemplate;
    private static final String EXTERNAL_SERVICE_URL = "https://api.example.com";

    public ExternalServiceClientImpl() {{
        this.restTemplate = new RestTemplate();
    }}

    @Override
    public Optional<String> fetchExternalData(String resourceId) {{
        try {{
            String url = EXTERNAL_SERVICE_URL + "/resources/" + resourceId;
            String response = restTemplate.getForObject(url, String.class);
            return Optional.ofNullable(response);
        }} catch (Exception e) {{
            return Optional.empty();
        }}
    }}

    @Override
    public void notifyExternalService(String eventType, String payload) {{
        try {{
            String url = EXTERNAL_SERVICE_URL + "/events";
            restTemplate.postForEntity(url, payload, Void.class);
        }} catch (Exception e) {{
            System.err.println("Failed to notify external service: " + e.getMessage());
        }}
    }}
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/outbound/restclient/ExternalServiceClientImpl.java", rest_client_impl_code)

        # Outbound Messaging: RabbitMQ Producer Implementation
        messaging_impl_code = f'''package {pkg}.outbound.messaging;

import {pkg}.domain.messaging.ExampleEventProducer;
import org.springframework.stereotype.Component;

/**
 * Message Producer Implementation (Outbound Adapter) - Publishes events to message broker.
 * Implements the domain messaging interface.
 * Example: RabbitMQ with RabbitTemplate
 */
@Component
public class RabbitMQExampleProducer implements ExampleEventProducer {{

    // @Autowired
    // private RabbitTemplate rabbitTemplate;

    private static final String EXCHANGE = "example.exchange";

    @Override
    public void publishExampleCreated(String exampleId, String name) {{
        String message = String.format("{{\\"event\\":\\"CREATED\\",\\"id\\":\\"%s\\",\\"name\\":\\"%s\\"}}", exampleId, name);
        // rabbitTemplate.convertAndSend(EXCHANGE, "example.created", message);
        System.out.println("Published event: " + message);
    }}

    @Override
    public void publishExampleDeleted(String exampleId) {{
        String message = String.format("{{\\"event\\":\\"DELETED\\",\\"id\\":\\"%s\\"}}", exampleId);
        // rabbitTemplate.convertAndSend(EXCHANGE, "example.deleted", message);
        System.out.println("Published event: " + message);
    }}
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/outbound/messaging/RabbitMQExampleProducer.java", messaging_impl_code)

        # ╔═══════════════════════════════════════════════════════════════╗
        # ║                      CONFIG                                   ║
        # ╚═══════════════════════════════════════════════════════════════╝

        # Application Config
        app_config_code = f'''package {pkg}.config;

import org.springframework.context.annotation.Configuration;

/**
 * Application Configuration - Beans, properties, etc.
 */
@Configuration
public class AppConfig {{

    // Define additional beans here
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/config/AppConfig.java", app_config_code)

        # Main Application Class
        main_app_code = f'''package {pkg};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {{

    public static void main(String[] args) {{
        SpringApplication.run(Application.class, args);
    }}
}}
'''
        self._write_java_file(base_path, f"{pkg_path}/Application.java", main_app_code)

        # application.properties
        props_path = base_path / "server/src/main/resources/application.properties"
        props_content = f"""# {config.name} - Spring Boot Configuration
server.port=8080
spring.application.name={self.project_name}

# Add your configuration here
"""
        with open(props_path, "w") as f:
            f.write(props_content)

        print("[green]Generated hexagonal architecture example![/green]")
        print("[dim]  INBOUND:  dto, rest (Controller), messaging (Consumer), security[/dim]")
        print("[dim]  DOMAIN:   model (Entity), service, repository, client, messaging (interfaces)[/dim]")
        print("[dim]  OUTBOUND: persistence (RepoImpl), restclient (ClientImpl), messaging (ProducerImpl)[/dim]")

    def _write_java_file(self, base_path: Path, relative_path: str, content: str) -> None:
        file_path = base_path / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)

    def install_dependencies(self, base_path: Path) -> None:
        server_path = base_path / "server"
        print("[yellow]Running mvn install...[/yellow]")
        try:
            subprocess.run(
                ["mvn", "install", "-DskipTests"],
                cwd=server_path,
                shell=True,
                check=True
            )
            print("[green]Java dependencies installed![/green]")
        except subprocess.CalledProcessError:
            print("[red]Maven build failed. Is 'mvn' installed and in PATH?[/red]")
        except Exception as e:
            print(f"[red]Error executing maven: {e}[/red]")

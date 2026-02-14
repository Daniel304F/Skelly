from pathlib import Path

from skelly.strategies.base import BackendStrategy
from skelly.core.models import Architecture, ProjectConfig
from skelly.core.template_renderer import render_to_file


class JavaSpringBackend(BackendStrategy):
    """Java Spring Boot backend with Maven."""

    DEPENDENCY_MAP = {
        "spring-boot-starter-security": ("org.springframework.boot", None),
        "spring-boot-starter-data-jpa": ("org.springframework.boot", None),
        "spring-boot-starter-actuator": ("org.springframework.boot", None),
        "lombok": ("org.projectlombok", "1.18.30"),
        "mapstruct": ("org.mapstruct", "1.5.5.Final"),
    }

    def __init__(self, project_name: str):
        self.project_name = project_name.lower().replace(" ", "")
        self.base_package = f"com.example.{self.project_name}"

    def get_folders(self) -> list[str]:
        return ["server/src/main/resources"]

    def get_name(self) -> str:
        return "Java Spring Boot"

    def create_config_files(self, config: ProjectConfig, base_path: Path) -> None:
        dependencies = []
        for lib in config.backend_libraries:
            dep_info = self.DEPENDENCY_MAP.get(lib)
            group_id = dep_info[0] if dep_info else "org.springframework.boot"
            version = dep_info[1] if dep_info else None
            dependencies.append({
                "group_id": group_id,
                "artifact_id": lib,
                "version": version,
            })

        render_to_file(
            "java_spring/pom.xml.j2",
            base_path / "server" / "pom.xml",
            project_name=self.project_name,
            dependencies=dependencies,
        )
        print("[cyan]Created server/pom.xml[/cyan]")

        if config.architecture == Architecture.HEXAGONAL.value:
            self._generate_hexagonal_example(config, base_path)

    def _generate_hexagonal_example(self, config: ProjectConfig, base_path: Path) -> None:
        """Generate example code with inbound/domain/outbound structure."""
        pkg = self.base_package
        pkg_path = f"server/src/main/java/{pkg.replace('.', '/')}"

        print("[cyan]Generating hexagonal architecture example (inbound/domain/outbound)...[/cyan]")

        template_file_map = {
            # Domain layer
            "java_spring/hexagonal/domain/Example.java.j2": f"{pkg_path}/domain/model/Example.java",
            "java_spring/hexagonal/domain/ExampleService.java.j2": f"{pkg_path}/domain/service/ExampleService.java",
            "java_spring/hexagonal/domain/ExampleRepository.java.j2": f"{pkg_path}/domain/repository/ExampleRepository.java",
            "java_spring/hexagonal/domain/ExternalServiceClient.java.j2": f"{pkg_path}/domain/client/ExternalServiceClient.java",
            "java_spring/hexagonal/domain/ExampleEventProducer.java.j2": f"{pkg_path}/domain/messaging/ExampleEventProducer.java",
            # Inbound layer
            "java_spring/hexagonal/inbound/ExampleRequest.java.j2": f"{pkg_path}/inbound/dto/ExampleRequest.java",
            "java_spring/hexagonal/inbound/ExampleResponse.java.j2": f"{pkg_path}/inbound/dto/ExampleResponse.java",
            "java_spring/hexagonal/inbound/ExampleController.java.j2": f"{pkg_path}/inbound/rest/ExampleController.java",
            "java_spring/hexagonal/inbound/ExampleMessageConsumer.java.j2": f"{pkg_path}/inbound/messaging/ExampleMessageConsumer.java",
            "java_spring/hexagonal/inbound/SecurityConfig.java.j2": f"{pkg_path}/inbound/security/SecurityConfig.java",
            # Outbound layer
            "java_spring/hexagonal/outbound/ExampleRepositoryImpl.java.j2": f"{pkg_path}/outbound/persistence/ExampleRepositoryImpl.java",
            "java_spring/hexagonal/outbound/ExternalServiceClientImpl.java.j2": f"{pkg_path}/outbound/restclient/ExternalServiceClientImpl.java",
            "java_spring/hexagonal/outbound/RabbitMQExampleProducer.java.j2": f"{pkg_path}/outbound/messaging/RabbitMQExampleProducer.java",
            # Config
            "java_spring/hexagonal/config/AppConfig.java.j2": f"{pkg_path}/config/AppConfig.java",
            "java_spring/hexagonal/Application.java.j2": f"{pkg_path}/Application.java",
        }

        for template, output in template_file_map.items():
            render_to_file(template, base_path / output, package=pkg)

        render_to_file(
            "java_spring/application.properties.j2",
            base_path / "server/src/main/resources/application.properties",
            project_name=self.project_name,
        )

        print("[green]Generated hexagonal architecture example![/green]")
        print("[dim]  INBOUND:  dto, rest (Controller), messaging (Consumer), security[/dim]")
        print("[dim]  DOMAIN:   model (Entity), service, repository, client, messaging (interfaces)[/dim]")
        print("[dim]  OUTBOUND: persistence (RepoImpl), restclient (ClientImpl), messaging (ProducerImpl)[/dim]")

    def install_dependencies(self, base_path: Path) -> None:
        server_path = base_path / "server"
        print("[yellow]Running mvn install...[/yellow]")
        self._run_command(
            ["mvn", "install", "-DskipTests"],
            cwd=server_path,
            success_msg="Java dependencies installed!",
            fail_msg="Maven build failed. Is 'mvn' installed and in PATH?",
        )

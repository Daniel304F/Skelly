import subprocess
from typing import List
from pathlib import Path

from skelly.strategies.base import BackendStrategy
from skelly.core.models import ProjectConfig


class JavaSpringBackend(BackendStrategy):
    """Java Spring Boot backend with Maven."""

    def __init__(self, project_name: str):
        self.project_name = project_name.lower().replace(" ", "")

    def get_folders(self) -> List[str]:
        return ["src/main/resources"]

    def get_name(self) -> str:
        return "Java Spring Boot"

    # Mapping: artifactId -> (groupId, version or None if managed by parent)
    DEPENDENCY_MAP = {
        # Spring Boot managed (no version needed)
        "spring-boot-starter-security": ("org.springframework.boot", None),
        "spring-boot-starter-data-jpa": ("org.springframework.boot", None),
        "spring-boot-starter-actuator": ("org.springframework.boot", None),
        # External dependencies (version required)
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
                # Default: assume Spring Boot starter
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
        pom_path = base_path / "pom.xml"
        with open(pom_path, "w") as f:
            f.write(pom_content.strip())

        print("[cyan]Created pom.xml[/cyan]")

    def install_dependencies(self, base_path: Path) -> None:
        print("[yellow]Running mvn install...[/yellow]")
        try:
            subprocess.run(
                ["mvn", "install", "-DskipTests"],
                cwd=base_path,
                shell=True,
                check=True
            )
            print("[green]Java dependencies installed![/green]")
        except subprocess.CalledProcessError:
            print("[red]Maven build failed. Is 'mvn' installed and in PATH?[/red]")
        except Exception as e:
            print(f"[red]Error executing maven: {e}[/red]")

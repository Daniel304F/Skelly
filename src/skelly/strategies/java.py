import subprocess
from typing import List
from pathlib import Path
from .base import ArchitectureStrategy
from skelly.core.models import ProjectConfig

class JavaHexagonalStrategy(ArchitectureStrategy):
    def __init__(self, project_name: str):
        self.project_name = project_name.lower().replace(" ", "")

    def get_architecture_name(self) -> str:
        return "Java Hexagonal Architecture"
    
    def get_required_folders(self) -> List[str]:
        base_pkg = f"src/main/java/com/example/{self.project_name}"
        return [
            f"{base_pkg}/domain/model",
            f"{base_pkg}/domain/service",
            f"{base_pkg}/application/port/in",
            f"{base_pkg}/application/port/out",
            f"{base_pkg}/adapter/in/web",
            f"{base_pkg}/adapter/out/persistence",
            "src/main/resources"
        ]

    def initialize_project(self, config: ProjectConfig, base_path: Path) -> None:
        # 1. dependencies in pom.xml
        dependencies_xml = ""
        
        for lib in config.backend_libraries:
            # Simple logic to guess GroupId to avoid mapping
            group_id = "org.springframework.boot" # Default for Spring Starter
            
            if lib == "lombok":
                group_id = "org.projectlombok"
            elif lib == "mapstruct":
                group_id = "org.mapstruct"
            
            # XML block creation
            dependencies_xml += f"""
        <dependency>
            <groupId>{group_id}</groupId>
            <artifactId>{lib}</artifactId>
        </dependency>"""

        # 2. creating pom.xml
        pom_content = f"""
<project xmlns="http://maven.apache.org/POM/4.0.0" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.example</groupId>
    <artifactId>{self.project_name}</artifactId>
    <version>0.0.1-SNAPSHOT</version>
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.1.2</version>
    </parent>

    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        {dependencies_xml}
    </dependencies>
</project>
"""
        with open(base_path / "pom.xml", "w") as f:
            f.write(pom_content.strip())
            
        print("[cyan]Created pom.xml[/cyan]")

        # 3. maven build execution
        print("[yellow]Running mvn install...[/yellow]")
        try:
            subprocess.run(["mvn", "install", "-DskipTests"], cwd=base_path, shell=True, check=True)
            print("[green]Java dependencies installed![/green]")
        except subprocess.CalledProcessError:
             print("[red]Maven build failed. Is 'mvn' installed and in PATH?[/red]")
        except Exception as e:
             print(f"[red]Error executing maven: {e}[/red]")
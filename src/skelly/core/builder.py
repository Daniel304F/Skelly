from typing import Optional
from pathlib import Path
import os
import traceback

from skelly.core.models import ProjectConfig
from skelly.strategies.base import ArchitectureStrategy


class ProjectBuilder:
    def __init__(self):
        self.config: Optional[ProjectConfig] = None

    def set_meta_data(self, name: str):
        self.config = ProjectConfig(name=name, frontend_stack="", backend_stack="")
        return self
    
    def set_frontend_stack(self, stack: str):
        if self.config:
            self.config.frontend_stack = stack
        return self
    
    def set_backend_stack(self, stack: str):
        if self.config:
            self.config.backend_stack = stack
        return self
    
    def set_architecture(self, architecture: str):
        if self.config:
            self.config.architecture = architecture
        return self
    
    def add_frontend_libraries(self, libraries: list[str]):
            if self.config:
                self.config.frontend_libraries.extend(libraries)
            return self

    def add_backend_libraries(self, libraries: list[str]):
            if self.config:
                self.config.backend_libraries.extend(libraries)
            return self
    
    def build(self, strategy: ArchitectureStrategy) -> ProjectConfig:
        if not self.config:
            raise ValueError("ProjectConfig is not initialized.")
        
        required_folders = strategy.get_required_folders() 

        print(f"Building project '{self.config.name}' with {strategy.get_architecture_name()}...")
        print(f"Creating folders: {required_folders}")

        ## Implement actual file system operations to create project structure
        base_path = Path(self.config.output_path) / self.config.name
        try:
            # root project folder 
            if not base_path.exists():
                os.makedirs(base_path)
                print(f"[green]Created project root at: {base_path.absolute()}[/green]")
            else:
                print(f"[yellow]Warning: Project folder '{base_path}' already exists.[/yellow]")
            required_folders = strategy.get_required_folders()
            print(f"[dim]Creating {len(required_folders)} folders...[/dim]")
            
            for folder in required_folders:
                full_path = base_path / folder
                os.makedirs(full_path, exist_ok=True)
                
                (full_path / ".gitkeep").touch()
            
            print("[green]Folder structure created successfully.[/green]")
            print("[dim]Initializing project dependencies...[/dim]")
            strategy.initialize_project(self.config, base_path)

        except PermissionError:
            print(f"[red]Error: Permission denied. Cannot write to {base_path}.[/red]")
        except Exception as e:
            print(f"[red]An unexpected error occurred during build:[/red]")
            print(f"[red]{e}[/red]")
            # Zeigt Details zum Fehler an (hilfreich bei subprocess Fehlern)
            traceback.print_exc()

        # Debug-Ausgabe des Config-Objekts am Ende
        print("\n[bold]Final Configuration:[/bold]")
        print(self.config)

        print(self.config)
        return self.config
    
    
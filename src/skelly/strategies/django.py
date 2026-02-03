import subprocess
from typing import List
from pathlib import Path
from .base import ArchitectureStrategy
from skelly.core.models import ProjectConfig

class DjangoStandardStrategy(ArchitectureStrategy):
    def __init__(self, project_name: str):
        self.project_name = project_name.lower().replace(" ", "_")

    def get_architecture_name(self) -> str:
        return "Django Standard Architecture"
    
    def get_required_folders(self) -> List[str]:
        return [
            self.project_name, 
            "static", 
            "media", 
            "templates"
        ]

    def initialize_project(self, config: ProjectConfig, base_path: Path) -> None:
        # requirements.txt 
        requirements = ["django>=4.2"]
        
        requirements.extend(config.backend_libraries)

        req_path = base_path / "requirements.txt"
        with open(req_path, "w") as f:
            f.write("\n".join(requirements))
        
        print(f"[cyan]Created requirements.txt with: {', '.join(config.backend_libraries)}[/cyan]")

        print("[yellow]Installing dependencies via pip...[/yellow]")
        try:
            subprocess.run(["pip", "install", "-r", "requirements.txt"], cwd=base_path, shell=True, check=True)
            
            
            print("[green]Django dependencies installed![/green]")
        except Exception as e:
            print(f"[red]Error with pip: {e}[/red]")
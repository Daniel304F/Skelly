from typing import List
from pathlib import Path
from .base import ArchitectureStrategy
from skelly.core.models import ProjectConfig

class CustomStrategy(ArchitectureStrategy):
    def __init__(self, folders: List[str]):
        self.custom_folders = folders

    def get_architecture_name(self) -> str:
        return "Custom Architecture"
    
    def get_required_folders(self) -> List[str]:
        return self.custom_folders

    def initialize_project(self, config: ProjectConfig, base_path: Path) -> None:
        print("[dim]Custom strategy selected: Skipping automated dependency installation.[/dim]")
        print(f"[dim]Libraries selected but not installed: {config.backend_libraries}[/dim]")
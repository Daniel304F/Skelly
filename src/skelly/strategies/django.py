from typing import List
from .base import ArchitectureStrategy

class DjangoStandardStrategy(ArchitectureStrategy):
    def __init__(self, project_name: str):
        self.project_name = project_name.lower().replace(" ", "_")

    def get_architecture_name(self) -> str:
        return "Django Standard Architecture"
    
    def get_required_folders(self) -> List[str]:
        return [
            self.project_name, # Der innere Konfigurations-Ordner (settings.py etc.)
            "static",
            "media",
            "templates"
        ]
from typing import List
from .base import ArchitectureStrategy

class JavaHexagonalStrategy(ArchitectureStrategy):
    def __init__(self, project_name: str):
        self.project_name = project_name.lower().replace(" ", "")

    def get_architecture_name(self) -> str:
        return "Java Hexagonal Architecture"
    
    def get_required_folders(self) -> List[str]:
        # Basis-Paketstruktur: src/main/java/com/firma/projektname
        base_path = f"src/main/java/com/firma/{self.project_name}"
        
        return [
            f"{base_path}/model",      # Domain / Core
            f"{base_path}/inbound",    # Driving Adapters
            f"{base_path}/outbound",   # Driven Adapters
            "src/main/resources"       # Standard Java Resource Folder
        ]
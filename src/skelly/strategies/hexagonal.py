from .base import ArchitectureStrategy
from typing import List

class HexagonalStrategy(ArchitectureStrategy):
    def get_architecture_name(self) -> str:
        return "Hexagonal Architecture"
    
    def get_required_folders(self) -> List[str]:

        return [
            "domain",
            "application",
            "infrastructure",
            "interfaces",
            "config",
        ]
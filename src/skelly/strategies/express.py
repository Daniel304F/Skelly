from typing import List
from .base import ArchitectureStrategy

class ExpressStandardStrategy(ArchitectureStrategy):
    def get_architecture_name(self) -> str:
        return "Express Standard Architecture"
    
    def get_required_folders(self) -> List[str]:
        return [
            "src/api/routes",
            "src/api/controllers",
            "src/api/middlewares",
            "src/services",
            "src/models",
            "src/loaders",
            "src/config",
            "src/utils"
        ]
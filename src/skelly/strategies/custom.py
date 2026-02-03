from typing import List
from .base import ArchitectureStrategy

class CustomStrategy(ArchitectureStrategy):
    def __init__(self, folders: List[str]):
        self.custom_folders = folders

    def get_architecture_name(self) -> str:
        return "Custom Architecture"
    
    def get_required_folders(self) -> List[str]:
        return self.custom_folders
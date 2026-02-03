from abc import ABC, abstractmethod
from typing import List
from skelly.core.models import ProjectConfig

class ArchitectureStrategy(ABC):
    @abstractmethod
    def get_required_folders(self) -> List[str]:
        """Return a list of required folder names for the architecture. """
        pass

    @abstractmethod
    def get_architecture_name(self) -> str:
        pass

    @abstractmethod
    def initialize_project(self, config: ProjectConfig, base_path: str) -> None:
        """
        Creates configuration files (package.json, pom.xml) and installs dependencies.
        """
        pass
from abc import ABC, abstractmethod
from typing import List

class ArchitectureStrategy(ABC):
    @abstractmethod
    def get_required_folders(self) -> List[str]:
        """Return a list of required folder names for the architecture. """
        pass

    @abstractmethod
    def get_architecture_name(self) -> str:
        pass
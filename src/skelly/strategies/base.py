from abc import ABC, abstractmethod
from typing import List
from pathlib import Path
from skelly.core.models import ProjectConfig


class ArchitectureStrategy(ABC):
    """
    Defines the folder structure for a project architecture.
    Only responsible for determining which folders to create.
    """

    @abstractmethod
    def get_folders(self) -> List[str]:
        """Return the list of folders that define this architecture."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the display name of this architecture."""
        pass


class BackendStrategy(ABC):
    """
    Handles backend-specific setup: configuration files and dependency installation.
    Separates the technology stack from the architectural pattern.
    """

    @abstractmethod
    def get_folders(self) -> List[str]:
        """Return backend-specific folders (e.g., src/main/resources for Java)."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the display name of this backend stack."""
        pass

    @abstractmethod
    def create_config_files(self, config: ProjectConfig, base_path: Path) -> None:
        """
        Create configuration files (pom.xml, package.json, requirements.txt).
        """
        pass

    @abstractmethod
    def install_dependencies(self, base_path: Path) -> None:
        """
        Install dependencies using the appropriate package manager.
        """
        pass


class FrontendStrategy(ABC):
    """
    Handles frontend-specific setup: folder structure, configuration, and dependencies.
    """

    @abstractmethod
    def get_folders(self) -> List[str]:
        """Return frontend-specific folders (e.g., src/components, src/hooks)."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the display name of this frontend stack."""
        pass

    @abstractmethod
    def create_config_files(self, config: ProjectConfig, base_path: Path) -> None:
        """
        Create frontend configuration files (package.json, vite.config.js, etc.).
        """
        pass

    @abstractmethod
    def install_dependencies(self, base_path: Path) -> None:
        """
        Install frontend dependencies using npm/yarn/pnpm.
        """
        pass

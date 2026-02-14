import logging
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

from skelly.core.models import ProjectConfig

logger = logging.getLogger(__name__)


class ArchitectureStrategy(ABC):
    """
    Defines the folder structure for a project architecture.
    Only responsible for determining which folders to create.
    """

    @abstractmethod
    def get_folders(self) -> list[str]:
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
    def get_folders(self) -> list[str]:
        """Return backend-specific folders (e.g., src/main/resources for Java)."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the display name of this backend stack."""
        pass

    @abstractmethod
    def create_config_files(self, config: ProjectConfig, base_path: Path) -> None:
        """Create configuration files (pom.xml, package.json, requirements.txt)."""
        pass

    @abstractmethod
    def install_dependencies(self, base_path: Path) -> None:
        """Install dependencies using the appropriate package manager."""
        pass

    @staticmethod
    def _run_command(
        cmd: list[str],
        cwd: Path,
        success_msg: str,
        fail_msg: str,
    ) -> None:
        """Run a shell command with standardized error handling."""
        try:
            subprocess.run(cmd, cwd=cwd, shell=True, check=True)
            print(f"[green]{success_msg}[/green]")
        except subprocess.CalledProcessError as e:
            logger.warning("Command %s failed with exit code %s", cmd, e.returncode)
            print(f"[red]{fail_msg}[/red]")
        except FileNotFoundError:
            logger.error("Command not found: %s", cmd[0])
            print(f"[red]{fail_msg}[/red]")
        except Exception as e:
            logger.exception("Unexpected error running %s", cmd)
            print(f"[red]Error: {e}[/red]")


class FrontendStrategy(ABC):
    """
    Handles frontend-specific setup: folder structure, configuration, and dependencies.
    """

    @abstractmethod
    def get_folders(self) -> list[str]:
        """Return frontend-specific folders (e.g., src/components, src/hooks)."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Return the display name of this frontend stack."""
        pass

    @abstractmethod
    def create_config_files(self, config: ProjectConfig, base_path: Path) -> None:
        """Create frontend configuration files (package.json, vite.config.js, etc.)."""
        pass

    def install_dependencies(self, base_path: Path) -> None:
        """Install frontend dependencies via npm."""
        frontend_path = base_path / "frontend"
        print("[yellow]Running npm install for frontend...[/yellow]")
        try:
            subprocess.run(["npm", "install"], cwd=frontend_path, shell=True, check=True)
            print("[green]Frontend dependencies installed![/green]")
        except subprocess.CalledProcessError as e:
            logger.warning("npm install failed with exit code %s", e.returncode)
            print("[red]Failed to install frontend dependencies. Do you have 'npm' installed?[/red]")
        except FileNotFoundError:
            logger.error("npm command not found")
            print("[red]Failed to install frontend dependencies. Do you have 'npm' installed?[/red]")
        except Exception as e:
            logger.exception("Unexpected error during frontend installation")
            print(f"[red]Error during frontend installation: {e}[/red]")

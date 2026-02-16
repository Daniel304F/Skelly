import logging
import os
from pathlib import Path

from skelly.core.exceptions import BuildError
from skelly.core.models import ProjectConfig
from skelly.strategies.base import ArchitectureStrategy, BackendStrategy, FrontendStrategy

logger = logging.getLogger(__name__)


class ProjectBuilder:
    """
    Builder pattern implementation for project scaffolding.
    Orchestrates architecture, backend, and frontend strategies.

    Collects configuration in mutable fields, then creates a frozen
    ProjectConfig at build time.
    """

    def __init__(self, dry_run: bool = False):
        self._name: str | None = None
        self._frontend_stack: str = ""
        self._backend_stack: str = ""
        self._architecture_name: str | None = None
        self._frontend_libraries: list[str] = []
        self._backend_libraries: list[str] = []
        self._output_path: str = "./"
        self._architecture: ArchitectureStrategy | None = None
        self._backend: BackendStrategy | None = None
        self._frontend: FrontendStrategy | None = None
        self._dry_run = dry_run

    def set_meta_data(self, name: str) -> "ProjectBuilder":
        self._name = name
        return self

    def set_frontend_stack(self, stack: str) -> "ProjectBuilder":
        self._frontend_stack = stack
        return self

    def set_backend_stack(self, stack: str) -> "ProjectBuilder":
        self._backend_stack = stack
        return self

    def set_architecture(self, architecture: str) -> "ProjectBuilder":
        self._architecture_name = architecture
        return self

    def add_frontend_libraries(self, libraries: list[str]) -> "ProjectBuilder":
        self._frontend_libraries.extend(libraries)
        return self

    def add_backend_libraries(self, libraries: list[str]) -> "ProjectBuilder":
        self._backend_libraries.extend(libraries)
        return self

    def with_architecture_strategy(self, strategy: ArchitectureStrategy) -> "ProjectBuilder":
        self._architecture = strategy
        return self

    def with_backend_strategy(self, strategy: BackendStrategy) -> "ProjectBuilder":
        self._backend = strategy
        return self

    def with_frontend_strategy(self, strategy: FrontendStrategy | None) -> "ProjectBuilder":
        self._frontend = strategy
        return self

    def _create_config(self) -> ProjectConfig:
        """Create an immutable ProjectConfig from the collected builder state."""
        return ProjectConfig(
            name=self._name,
            frontend_stack=self._frontend_stack,
            backend_stack=self._backend_stack,
            architecture=self._architecture_name,
            frontend_libraries=tuple(self._frontend_libraries),
            backend_libraries=tuple(self._backend_libraries),
            output_path=self._output_path,
        )

    def build(self) -> ProjectConfig:
        if not self._name:
            raise BuildError("Project name is not set. Call set_meta_data() first.")

        if not self._architecture:
            raise BuildError("Architecture strategy is required. Call with_architecture_strategy() first.")

        config = self._create_config()

        if self._dry_run:
            return self._build_dry_run(config)

        print(f"\n[bold]Building project '{config.name}'...[/bold]")
        print(f"  Architecture: {self._architecture.get_name()}")
        if self._backend:
            print(f"  Backend: {self._backend.get_name()}")
        if self._frontend:
            print(f"  Frontend: {self._frontend.get_name()}")

        base_path = Path(config.output_path) / config.name

        try:
            self._create_root_directory(base_path)
            self._create_folder_structure(base_path)
            self._setup_backend(config, base_path)
            self._setup_frontend(config, base_path)
        except PermissionError:
            logger.exception("Permission denied for %s", base_path)
            print(f"[red]Error: Permission denied. Cannot write to {base_path}.[/red]")
        except BuildError:
            raise
        except Exception as e:
            logger.exception("Unexpected error during build")
            print(f"[red]An unexpected error occurred during build: {e}[/red]")

        print("\n[bold]Final Configuration:[/bold]")
        print(config)

        return config

    def _build_dry_run(self, config: ProjectConfig) -> ProjectConfig:
        """Preview what would be created without writing any files."""
        print("\n[bold yellow]DRY RUN — No files will be created.[/bold yellow]")
        print(f"\n[bold]Project: '{config.name}'[/bold]")
        print(f"  Architecture: {self._architecture.get_name()}")
        if self._backend:
            print(f"  Backend: {self._backend.get_name()}")
        if self._frontend:
            print(f"  Frontend: {self._frontend.get_name()}")

        base_path = Path(config.output_path) / config.name
        all_folders = self._collect_all_folders()

        print(f"\n[bold]Would create {len(all_folders)} folders under {base_path}:[/bold]")
        for folder in sorted(all_folders):
            print(f"  [dim]{folder}/[/dim]")

        if config.backend_libraries:
            print(f"\n[bold]Backend libraries:[/bold] {', '.join(config.backend_libraries)}")
        if config.frontend_libraries:
            print(f"[bold]Frontend libraries:[/bold] {', '.join(config.frontend_libraries)}")

        return config

    def _create_root_directory(self, base_path: Path) -> None:
        if not base_path.exists():
            os.makedirs(base_path)
            print(f"[green]Created project root at: {base_path.absolute()}[/green]")
        else:
            print(f"[yellow]Warning: Project folder '{base_path}' already exists.[/yellow]")

    def _create_folder_structure(self, base_path: Path) -> None:
        all_folders = self._collect_all_folders()
        print(f"\n[dim]Creating {len(all_folders)} folders...[/dim]")
        for folder in all_folders:
            full_path = base_path / folder
            os.makedirs(full_path, exist_ok=True)
            (full_path / ".gitkeep").touch()
        print("[green]Folder structure created successfully.[/green]")

    def _setup_backend(self, config: ProjectConfig, base_path: Path) -> None:
        if not self._backend:
            return
        print(f"\n[bold]Setting up {self._backend.get_name()} backend...[/bold]")
        self._backend.create_config_files(config, base_path)
        self._backend.install_dependencies(base_path)

    def _setup_frontend(self, config: ProjectConfig, base_path: Path) -> None:
        if not self._frontend:
            return
        print(f"\n[bold]Setting up {self._frontend.get_name()} frontend...[/bold]")
        self._frontend.create_config_files(config, base_path)
        self._frontend.install_dependencies(base_path)

    def _collect_all_folders(self) -> list[str]:
        folders = list(self._architecture.get_folders())
        if self._backend:
            folders.extend(self._backend.get_folders())
        if self._frontend:
            folders.extend(self._frontend.get_folders())
        return folders

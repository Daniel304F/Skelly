import subprocess
from typing import List
from pathlib import Path

from skelly.strategies.base import BackendStrategy
from skelly.core.models import ProjectConfig


class DjangoBackend(BackendStrategy):
    """Django backend with pip."""

    def get_folders(self) -> List[str]:
        return []

    def get_name(self) -> str:
        return "Django"

    def create_config_files(self, config: ProjectConfig, base_path: Path) -> None:
        server_path = base_path / "server"
        requirements = ["django>=4.2"]
        requirements.extend(config.backend_libraries)

        req_path = server_path / "requirements.txt"
        with open(req_path, "w") as f:
            f.write("\n".join(requirements))

        print(f"[cyan]Created server/requirements.txt with: {', '.join(requirements)}[/cyan]")

    def install_dependencies(self, base_path: Path) -> None:
        server_path = base_path / "server"
        print("[yellow]Installing server dependencies via pip...[/yellow]")
        try:
            subprocess.run(
                ["pip", "install", "-r", "requirements.txt"],
                cwd=server_path,
                shell=True,
                check=True
            )
            print("[green]Django dependencies installed![/green]")
        except Exception as e:
            print(f"[red]Error with pip: {e}[/red]")

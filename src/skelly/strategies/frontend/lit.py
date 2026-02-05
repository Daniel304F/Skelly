import json
import subprocess
from typing import List
from pathlib import Path

from skelly.strategies.base import FrontendStrategy
from skelly.core.models import ProjectConfig


class LitFrontend(FrontendStrategy):
    """Lit web components frontend with Vite and npm."""

    def get_folders(self) -> List[str]:
        return [
            "frontend/src/components",
            "frontend/src/styles",
            "frontend/public"
        ]

    def get_name(self) -> str:
        return "Lit"

    def create_config_files(self, config: ProjectConfig, base_path: Path) -> None:
        frontend_path = base_path / "frontend"

        dependencies = {
            "lit": "^3.1.0"
        }

        dev_dependencies = {
            "vite": "^5.0.0"
        }

        # Library entries may contain multiple packages separated by spaces
        for lib_entry in config.frontend_libraries:
            packages = lib_entry.split()
            for pkg in packages:
                dependencies[pkg] = "latest"

        package_json = {
            "name": f"{config.name.lower().replace(' ', '-')}-frontend",
            "private": True,
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "dependencies": dependencies,
            "devDependencies": dev_dependencies
        }

        package_json_path = frontend_path / "package.json"
        with open(package_json_path, "w") as f:
            json.dump(package_json, f, indent=2)

        vite_config = """import { defineConfig } from 'vite'

export default defineConfig({
  build: {
    lib: {
      entry: 'src/index.js',
      formats: ['es']
    }
  }
})
"""
        vite_config_path = frontend_path / "vite.config.js"
        with open(vite_config_path, "w") as f:
            f.write(vite_config)

        index_html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{config.name}</title>
  </head>
  <body>
    <my-app></my-app>
    <script type="module" src="/src/index.js"></script>
  </body>
</html>
"""
        index_path = frontend_path / "index.html"
        with open(index_path, "w") as f:
            f.write(index_html)

        print(f"[cyan]Created Lit frontend config with: {', '.join(dependencies.keys())}[/cyan]")

    def install_dependencies(self, base_path: Path) -> None:
        frontend_path = base_path / "frontend"
        print("[yellow]Running npm install for frontend...[/yellow]")
        try:
            subprocess.run(["npm", "install"], cwd=frontend_path, shell=True, check=True)
            print("[green]Frontend dependencies installed![/green]")
        except subprocess.CalledProcessError:
            print("[red]Failed to install frontend dependencies. Do you have 'npm' installed?[/red]")
        except Exception as e:
            print(f"[red]Error during frontend installation: {e}[/red]")

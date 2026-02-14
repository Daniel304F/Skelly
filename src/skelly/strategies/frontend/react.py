import json
from pathlib import Path

from skelly.strategies.base import FrontendStrategy
from skelly.core.models import ProjectConfig


class ReactFrontend(FrontendStrategy):
    """React frontend with Vite and npm."""

    def get_folders(self) -> list[str]:
        return [
            "frontend/src/components",
            "frontend/src/hooks",
            "frontend/src/pages",
            "frontend/src/services",
            "frontend/src/assets",
            "frontend/public",
        ]

    def get_name(self) -> str:
        return "React"

    def create_config_files(self, config: ProjectConfig, base_path: Path) -> None:
        frontend_path = base_path / "frontend"

        dependencies = {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
        }

        dev_dependencies = {
            "@vitejs/plugin-react": "^4.2.0",
            "vite": "^5.0.0",
        }

        for lib_entry in config.frontend_libraries:
            packages = lib_entry.split()
            for pkg in packages:
                if pkg in ["tailwindcss", "postcss", "autoprefixer"]:
                    dev_dependencies[pkg] = "latest"
                else:
                    dependencies[pkg] = "latest"

        package_json = {
            "name": f"{config.name.lower().replace(' ', '-')}-frontend",
            "private": True,
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview",
            },
            "dependencies": dependencies,
            "devDependencies": dev_dependencies,
        }

        package_json_path = frontend_path / "package.json"
        with open(package_json_path, "w") as f:
            json.dump(package_json, f, indent=2)

        vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
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
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""
        index_path = frontend_path / "index.html"
        with open(index_path, "w") as f:
            f.write(index_html)

        print(f"[cyan]Created React frontend config with: {', '.join(dependencies.keys())}[/cyan]")

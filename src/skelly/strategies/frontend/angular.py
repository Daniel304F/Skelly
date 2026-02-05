import json
import subprocess
from typing import List
from pathlib import Path

from skelly.strategies.base import FrontendStrategy
from skelly.core.models import ProjectConfig


class AngularFrontend(FrontendStrategy):
    """Angular frontend with Angular CLI."""

    def get_folders(self) -> List[str]:
        return [
            "frontend/src/app/components",
            "frontend/src/app/services",
            "frontend/src/app/pages",
            "frontend/src/assets",
            "frontend/src/environments"
        ]

    def get_name(self) -> str:
        return "Angular"

    def create_config_files(self, config: ProjectConfig, base_path: Path) -> None:
        frontend_path = base_path / "frontend"

        dependencies = {
            "@angular/animations": "^17.0.0",
            "@angular/common": "^17.0.0",
            "@angular/compiler": "^17.0.0",
            "@angular/core": "^17.0.0",
            "@angular/forms": "^17.0.0",
            "@angular/platform-browser": "^17.0.0",
            "@angular/platform-browser-dynamic": "^17.0.0",
            "@angular/router": "^17.0.0",
            "rxjs": "~7.8.0",
            "tslib": "^2.6.0",
            "zone.js": "~0.14.0"
        }

        dev_dependencies = {
            "@angular-devkit/build-angular": "^17.0.0",
            "@angular/cli": "^17.0.0",
            "@angular/compiler-cli": "^17.0.0",
            "typescript": "~5.2.0"
        }

        # Library entries may contain multiple packages separated by spaces
        for lib_entry in config.frontend_libraries:
            packages = lib_entry.split()
            for pkg in packages:
                dependencies[pkg] = "latest"

        package_json = {
            "name": f"{config.name.lower().replace(' ', '-')}-frontend",
            "version": "0.1.0",
            "scripts": {
                "ng": "ng",
                "start": "ng serve",
                "build": "ng build",
                "test": "ng test"
            },
            "dependencies": dependencies,
            "devDependencies": dev_dependencies
        }

        package_json_path = frontend_path / "package.json"
        with open(package_json_path, "w") as f:
            json.dump(package_json, f, indent=2)

        angular_json = {
            "$schema": "./node_modules/@angular/cli/lib/config/schema.json",
            "version": 1,
            "newProjectRoot": "projects",
            "projects": {
                config.name.lower().replace(" ", "-"): {
                    "projectType": "application",
                    "root": "",
                    "sourceRoot": "src",
                    "architect": {
                        "build": {
                            "builder": "@angular-devkit/build-angular:application",
                            "options": {
                                "outputPath": "dist",
                                "index": "src/index.html",
                                "browser": "src/main.ts",
                                "tsConfig": "tsconfig.json"
                            }
                        },
                        "serve": {
                            "builder": "@angular-devkit/build-angular:dev-server"
                        }
                    }
                }
            }
        }

        angular_json_path = frontend_path / "angular.json"
        with open(angular_json_path, "w") as f:
            json.dump(angular_json, f, indent=2)

        index_html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{config.name}</title>
    <base href="/" />
  </head>
  <body>
    <app-root></app-root>
  </body>
</html>
"""
        src_path = frontend_path / "src"
        src_path.mkdir(parents=True, exist_ok=True)
        index_path = src_path / "index.html"
        with open(index_path, "w") as f:
            f.write(index_html)

        print(f"[cyan]Created Angular frontend config[/cyan]")

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

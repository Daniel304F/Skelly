import argparse

import questionary
from rich.console import Console

from skelly.core.builder import ProjectBuilder
from skelly.core.models import Architecture, BackendStack, FrontendStack
from skelly.factories.base import StrategyFactory
from skelly.factories.frontend_factory import FrontendFactory
from skelly.factories.backend_factory import BackendFactory

console = Console()


def _ask_project_name() -> str | None:
    project_name = questionary.text("Enter the project name:").ask()
    if not project_name:
        console.print("[red]Project name is required.[/red]")
        return None
    return project_name


def _ask_stacks() -> tuple[FrontendStack, BackendStack]:
    frontend_value = questionary.select(
        "Choose a frontend stack:",
        choices=[
            questionary.Choice(s.value, value=s) for s in FrontendStack
        ],
    ).ask()

    backend_value = questionary.select(
        "Choose a backend stack:",
        choices=[
            questionary.Choice(s.value, value=s) for s in BackendStack
        ],
    ).ask()

    return frontend_value, backend_value


def _ask_libraries(
    frontend_stack: FrontendStack, backend_stack: BackendStack
) -> tuple[list[str], list[str]]:
    frontend_libs = []
    if frontend_stack != FrontendStack.NONE:
        frontend_libs = questionary.checkbox(
            f"Select libraries for {frontend_stack.value}:",
            choices=FrontendFactory.get_supported_libraries(frontend_stack),
        ).ask() or []

    backend_libs = questionary.checkbox(
        f"Select libraries for {backend_stack.value}:",
        choices=BackendFactory.get_supported_libraries(backend_stack),
    ).ask() or []

    return frontend_libs, backend_libs


def _ask_architecture() -> tuple[str, list[str] | None]:
    arch_options = [
        questionary.Choice(Architecture.HEXAGONAL.value, value="hexagonal"),
        questionary.Choice(Architecture.LAYERED.value, value="layered"),
        questionary.Choice("Custom Structure", value="custom"),
    ]

    choice = questionary.select(
        "Choose an architecture pattern:",
        choices=arch_options,
    ).ask()

    custom_folders = None
    if choice == "custom":
        console.print("[yellow]Please enter folder paths separated by commas.[/yellow]")
        console.print("[dim]Example: src/controllers, src/models, utils[/dim]")
        folders_input = questionary.text("Enter folders:").ask()
        custom_folders = [f.strip() for f in folders_input.split(",") if f.strip()]

    return choice, custom_folders


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="skelly",
        description="Project scaffolding with separated concerns",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the project structure without creating any files",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    console.print("[bold green]Welcome to the Skelly CLI![/bold green]")
    console.print("[dim]Project scaffolding with separated concerns[/dim]\n")

    if args.dry_run:
        console.print("[yellow]Running in dry-run mode — no files will be created.[/yellow]\n")

    project_name = _ask_project_name()
    if not project_name:
        return

    frontend_stack, backend_stack = _ask_stacks()
    frontend_libs, backend_libs = _ask_libraries(frontend_stack, backend_stack)
    arch_choice, custom_folders = _ask_architecture()

    architecture_strategy = StrategyFactory.create_architecture(
        arch_choice, project_name, backend_stack, custom_folders
    )
    backend_strategy = StrategyFactory.create_backend(backend_stack, project_name)
    frontend_strategy = StrategyFactory.create_frontend(frontend_stack)

    builder = ProjectBuilder(dry_run=args.dry_run)
    builder.set_meta_data(project_name)\
           .set_frontend_stack(frontend_stack.value)\
           .set_backend_stack(backend_stack.value)\
           .set_architecture(architecture_strategy.get_name())\
           .add_frontend_libraries(frontend_libs)\
           .add_backend_libraries(backend_libs)\
           .with_architecture_strategy(architecture_strategy)\
           .with_backend_strategy(backend_strategy)\
           .with_frontend_strategy(frontend_strategy)

    builder.build()

    if not args.dry_run:
        console.print("\n[bold green]Project scaffolding complete![/bold green]")


if __name__ == "__main__":
    main()

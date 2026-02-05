import questionary
from rich.console import Console

from skelly.core.builder import ProjectBuilder
from skelly.factories.frontend_factory import FrontendFactory
from skelly.factories.backend_factory import BackendFactory

# Architecture strategies
from skelly.strategies.architecture import (
    HexagonalArchitecture,
    LayeredArchitecture,
    CustomArchitecture
)

# Backend strategies
from skelly.strategies.backend import (
    JavaSpringBackend,
    ExpressBackend,
    DjangoBackend
)

# Frontend strategies
from skelly.strategies.frontend import (
    ReactFrontend,
    LitFrontend,
    AngularFrontend
)

console = Console()


def main() -> None:
    console.print("[bold green]Welcome to the Skelly CLI![/bold green]")
    console.print("[dim]Project scaffolding with separated concerns[/dim]\n")

    # Project metadata
    project_name = questionary.text("Enter the project name:").ask()
    if not project_name:
        console.print("[red]Project name is required.[/red]")
        return

    # Stack selection
    frontend_stack = questionary.select(
        "Choose a frontend stack:",
        choices=["React", "Lit", "Angular", "None (Backend only)"]
    ).ask()

    backend_stack = questionary.select(
        "Choose a backend stack:",
        choices=["Java", "Express", "Django"]
    ).ask()

    # Library selection
    frontend_libs = []
    if frontend_stack != "None (Backend only)":
        frontend_libs = questionary.checkbox(
            f"Select libraries for {frontend_stack}:",
            choices=FrontendFactory.get_supported_libraries(frontend_stack)
        ).ask() or []

    backend_libs = questionary.checkbox(
        f"Select libraries for {backend_stack}:",
        choices=BackendFactory.get_supported_libraries(backend_stack)
    ).ask() or []

    # Architecture selection (independent of backend!)
    arch_options = [
        questionary.Choice("Hexagonal Architecture", value="hexagonal"),
        questionary.Choice("Layered Architecture", value="layered"),
        questionary.Choice("Custom Structure", value="custom")
    ]

    architecture_choice = questionary.select(
        "Choose an architecture pattern:",
        choices=arch_options
    ).ask()

    # Create architecture strategy
    architecture_strategy = None

    if architecture_choice == "custom":
        console.print("[yellow]Please enter folder paths separated by commas.[/yellow]")
        console.print("[dim]Example: src/controllers, src/models, utils[/dim]")

        folders_input = questionary.text("Enter folders:").ask()
        folder_list = [f.strip() for f in folders_input.split(",") if f.strip()]
        architecture_strategy = CustomArchitecture(folder_list)

    elif architecture_choice == "hexagonal":
        base_package = "src"
        if backend_stack == "Java":
            base_package = "java"
        architecture_strategy = HexagonalArchitecture(project_name, base_package)

    elif architecture_choice == "layered":
        architecture_strategy = LayeredArchitecture()

    # Create backend strategy
    backend_strategy = None

    if backend_stack == "Java":
        backend_strategy = JavaSpringBackend(project_name)
    elif backend_stack == "Express":
        backend_strategy = ExpressBackend()
    elif backend_stack == "Django":
        backend_strategy = DjangoBackend()

    # Create frontend strategy
    frontend_strategy = None

    if frontend_stack == "React":
        frontend_strategy = ReactFrontend()
    elif frontend_stack == "Lit":
        frontend_strategy = LitFrontend()
    elif frontend_stack == "Angular":
        frontend_strategy = AngularFrontend()

    # Build the project
    builder = ProjectBuilder()
    builder.set_meta_data(project_name)\
           .set_frontend_stack(frontend_stack)\
           .set_backend_stack(backend_stack)\
           .set_architecture(architecture_strategy.get_name())\
           .add_frontend_libraries(frontend_libs)\
           .add_backend_libraries(backend_libs)\
           .with_architecture_strategy(architecture_strategy)\
           .with_backend_strategy(backend_strategy)\
           .with_frontend_strategy(frontend_strategy)

    builder.build()

    console.print("\n[bold green]Project scaffolding complete![/bold green]")


if __name__ == "__main__":
    main()

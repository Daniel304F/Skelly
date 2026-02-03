import questionary
from rich.console import Console

from skelly.core.builder import ProjectBuilder
from skelly.factories.frontend_factory import FrontendFactory
from skelly.factories.backend_factory import BackendFactory
from skelly.strategies.hexagonal import HexagonalStrategy

console = Console()

def main() -> None:
    console.print("[bold green]Welcome to the Skelly CLI![/bold green]")

# Metadata, stacks
    project_name = questionary.text("Enter the project name:").ask()
    frontend_stack = questionary.select("Choose a frontend stack:", choices=["React", "Lit", "Angular"]).ask()
    backend_stack = questionary.select("Choose a backend stack:", choices=["Java", "Express", "Django"]).ask()

## Frontend library selection based on chosen frontend stack
    frontend_libs = questionary.checkbox(
            f"Select libraries for {frontend_stack}:",
            choices=FrontendFactory.get_supported_libraries(frontend_stack)
        ).ask()

## Backend library selection based on backend stack    
    backend_libs = questionary.checkbox(
            f"Select libraries for {backend_stack}:",
            choices=BackendFactory.get_supported_libraries(backend_stack)
        ).ask()

## Basic selection for archticture and strategy
    strategy = None # For now none
    architecture_choice = "custom"

    if backend_stack in ["Java", "Express"]:
        architecture_choice = questionary.select(
            "Choose a strategy:",
            choices=["custom", "hexagonal"]
        ).ask()

        if architecture_choice == "hexagonal":
            strategy = HexagonalStrategy()
        if architecture_choice == "custom":
            strategy = None  # Custom strategy to be implemented
    else:
        console.print(f"[dim]Using standard structure for {backend_stack}[/dim]")
        strategy = None # StandardStrategy() Must be implemented


    architecture = questionary.select("Choose an architecture:", choices=["", "hexagonal"]).ask()

    ## Choosen frontend libraries depending on selected frontend stack

    ## To-Do: Implement backend library selection based on chosen backend stack

    builder = ProjectBuilder()
    builder.set_meta_data(project_name)\
            .set_frontend_stack(frontend_stack)\
            .set_backend_stack(backend_stack)\
            .set_architecture(architecture)\
            .add_frontend_libraries(frontend_libs)\
            .add_backend_libraries(backend_libs)
    
    builder.build(strategy=strategy)
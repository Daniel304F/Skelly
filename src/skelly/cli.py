import questionary
from rich.console import Console

from skelly.core.builder import ProjectBuilder
from skelly.factories.frontend_factory import FrontendFactory
from skelly.factories.backend_factory import BackendFactory
from skelly.strategies.custom import CustomStrategy
from skelly.strategies.django import DjangoStandardStrategy
from skelly.strategies.express import ExpressStandardStrategy
from skelly.strategies.hexagonal import HexagonalStrategy
from skelly.strategies.java import JavaHexagonalStrategy

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
    arch_options = ["Custom Structure"]
        
    if backend_stack == "Java":
            arch_options.insert(0, "Hexagonal Architecture")
    elif backend_stack == "Express":
            arch_options.insert(0, "Standard Express (Layered)")
    elif backend_stack == "Django":
            arch_options.insert(0, "Django Default")

    architecture_choice = questionary.select(
        f"Choose an architecture strategy for backend: {backend_stack}",
        choices=arch_options
    ).ask()

    if architecture_choice == "Custom Structure":
            console.print("[yellow]Please enter folder paths separated by commas.[/yellow]")
            console.print("[dim]Example: src/controllers, src/models, utils[/dim]")
            
            folders_input = questionary.text("Enter folders:").ask()
            
            folder_list = [f.strip() for f in folders_input.split(",") if f.strip()]
            strategy = CustomStrategy(folder_list)

    elif architecture_choice == "Hexagonal Architecture" and backend_stack == "Java":
        strategy = JavaHexagonalStrategy(project_name)

    elif architecture_choice == "Standard Express (Layered)" and backend_stack == "Express":
        strategy = ExpressStandardStrategy()

    elif architecture_choice == "Django Default" and backend_stack == "Django":
        strategy = DjangoStandardStrategy(project_name)
    
    else:
        # fallback
        console.print("[red]No valid strategy found via selection logic.[/red]")
        return

    builder = ProjectBuilder()
    builder.set_meta_data(project_name)\
            .set_frontend_stack(frontend_stack)\
            .set_backend_stack(backend_stack)\
            .set_architecture(strategy.get_architecture_name())\
            .add_frontend_libraries(frontend_libs)\
            .add_backend_libraries(backend_libs)
    
    builder.build(strategy=strategy)
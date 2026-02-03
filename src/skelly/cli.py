import questionary
from rich.console import Console

from skelly.core.builder import ProjectBuilder

console = Console()

def main() -> None:
    console.print("[bold green]Welcome to the Skelly CLI![/bold green]")

    project_name = questionary.text("Enter the project name:").ask()
    frontend_stack = questionary.select("Choose a frontend stack:", choices=["React", "Lit", "Angular"]).ask()
    backend_stack = questionary.select("Choose a backend stack:", choices=["Java", "Express", "Django"]).ask()

    ## To-Do: Available architecture options should depend on selected stacks
    ## For every stack combination, it is possible that no architecture or your own custom architecture is available
    architecture = questionary.select("Choose an architecture:", choices=["", "hexagonal"]).ask()

    ## To-Do: Implement frontend library selection based on chosen frontend stack

    ## To-Do: Implement backend library selection based on chosen backend stack

    builder = ProjectBuilder()
    builder.set_meta_data(project_name).set_frontend_stack(frontend_stack).set_backend_stack(backend_stack).set_architecture(architecture).build(strategy=None)
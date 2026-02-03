from typing import Optional

from skelly.core.models import ProjectConfig
from skelly.strategies.base import ArchitectureStrategy


class ProjectBuilder:
    def __init__(self):
        self.config: Optional[ProjectConfig] = None

    def set_meta_data(self, name: str):
        self.config = ProjectConfig(name=name, frontend_stack="", backend_stack="")
        return self
    
    def set_frontend_stack(self, stack: str):
        if self.config:
            self.config.frontend_stack = stack
        return self
    
    def set_backend_stack(self, stack: str):
        if self.config:
            self.config.backend_stack = stack
        return self
    
    def set_architecture(self, architecture: str):
        if self.config:
            self.config.architecture = architecture
        return self
    
    def add_frontend_libraries(self, libraries: list[str]):
            if self.config:
                self.config.frontend_libraries.extend(libraries)
            return self

    def add_backend_libraries(self, libraries: list[str]):
            if self.config:
                self.config.backend_libraries.extend(libraries)
            return self
    
    def build(self, strategy: ArchitectureStrategy) -> ProjectConfig:
        if not self.config:
            raise ValueError("ProjectConfig is not initialized.")
        
        required_folders = strategy.get_required_folders() 

        print(f"Building project '{self.config.name}' with {strategy.get_architecture_name()}...")
        print(f"Creating folders: {required_folders}")

        ## To-Do: Implement actual file system operations to create project structure


        print(self.config)
        return self.config
    
    
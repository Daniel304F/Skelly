from typing import Optional

from skelly.core.models import ProjectConfig


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
    
    def add_library(self, library: str):
        if self.config:
            self.config.libraries.append(library)
        return self
    
    def build(self) -> Optional[ProjectConfig]:
        return self.config
    
    
from dataclasses import dataclass, field
from enum import Enum


class FrontendStack(Enum):
    REACT = "React"
    LIT = "Lit"
    ANGULAR = "Angular"
    NONE = "None (Backend only)"


class BackendStack(Enum):
    JAVA = "Java"
    EXPRESS = "Express"
    DJANGO = "Django"


class Architecture(Enum):
    HEXAGONAL = "Hexagonal Architecture"
    LAYERED = "Layered Architecture"
    CUSTOM = "Custom Architecture"


@dataclass
class ProjectConfig:
    name: str
    frontend_stack: str
    backend_stack: str
    architecture: str | None = None
    frontend_libraries: list[str] = field(default_factory=list)
    backend_libraries: list[str] = field(default_factory=list)
    output_path: str = "./"

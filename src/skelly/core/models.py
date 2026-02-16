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


@dataclass(frozen=True)
class ProjectConfig:
    name: str
    frontend_stack: str
    backend_stack: str
    architecture: str | None = None
    frontend_libraries: tuple[str, ...] = ()
    backend_libraries: tuple[str, ...] = ()
    output_path: str = "./"

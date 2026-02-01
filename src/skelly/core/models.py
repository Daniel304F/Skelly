from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ProjectConfig:
    name: str
    frontend_stack: str
    backend_stack: str
    architecture: Optional[str] = None
    libraries: List[str] = field(default_factory=list)
    output_path: str = "./"


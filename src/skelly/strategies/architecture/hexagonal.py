from typing import List

from skelly.strategies.base import ArchitectureStrategy


class HexagonalArchitecture(ArchitectureStrategy):
    """
    Hexagonal Architecture (Ports and Adapters).
    Supports multiple backends: Java, TypeScript/Node, etc.
    """

    def __init__(self, project_name: str, base_package: str = "src"):
        self.project_name = project_name.lower().replace(" ", "")
        self.base_package = base_package

    def get_folders(self) -> List[str]:
        base = self.base_package

        if self.base_package == "java":
            base = f"src/main/java/com/example/{self.project_name}"

        return [
            f"{base}/domain/model",
            f"{base}/domain/service",
            f"{base}/application/port/in",
            f"{base}/application/port/out",
            f"{base}/application/service",
            f"{base}/adapter/in/web",
            f"{base}/adapter/out/persistence",
            f"{base}/infrastructure/config"
        ]

    def get_name(self) -> str:
        return "Hexagonal Architecture"

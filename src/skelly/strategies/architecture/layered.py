from typing import List

from skelly.strategies.base import ArchitectureStrategy


class LayeredArchitecture(ArchitectureStrategy):
    """
    Traditional Layered Architecture.
    Common structure for Express, Django, and similar frameworks.
    """

    def __init__(self, base_path: str = "src"):
        self.base_path = base_path

    def get_folders(self) -> List[str]:
        base = f"server/{self.base_path}"
        return [
            f"{base}/api/routes",
            f"{base}/api/controllers",
            f"{base}/api/middlewares",
            f"{base}/services",
            f"{base}/models",
            f"{base}/repositories",
            f"{base}/config",
            f"{base}/utils"
        ]

    def get_name(self) -> str:
        return "Layered Architecture"

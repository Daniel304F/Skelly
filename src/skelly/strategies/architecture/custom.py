from skelly.strategies.base import ArchitectureStrategy


class CustomArchitecture(ArchitectureStrategy):
    """
    Custom user-defined folder structure.
    Allows full flexibility while still benefiting from backend/frontend strategies.
    """

    def __init__(self, folders: list[str]):
        self.custom_folders = folders

    def get_folders(self) -> list[str]:
        return self.custom_folders

    def get_name(self) -> str:
        return "Custom Architecture"

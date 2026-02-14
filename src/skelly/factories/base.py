from skelly.core.models import Architecture, BackendStack, FrontendStack
from skelly.strategies.base import ArchitectureStrategy, BackendStrategy, FrontendStrategy
from skelly.strategies.architecture import (
    HexagonalArchitecture,
    LayeredArchitecture,
    CustomArchitecture,
)
from skelly.strategies.backend import (
    JavaSpringBackend,
    ExpressBackend,
    DjangoBackend,
)
from skelly.strategies.frontend import (
    ReactFrontend,
    LitFrontend,
    AngularFrontend,
)


class StrategyFactory:
    """Creates strategy instances based on user selections."""

    @staticmethod
    def create_architecture(
        choice: str,
        project_name: str,
        backend_stack: BackendStack,
        custom_folders: list[str] | None = None,
    ) -> ArchitectureStrategy:
        if choice == "custom":
            return CustomArchitecture(custom_folders or [])
        if choice == "hexagonal":
            base_package = "java" if backend_stack == BackendStack.JAVA else "src"
            return HexagonalArchitecture(project_name, base_package)
        if choice == "layered":
            return LayeredArchitecture()
        raise ValueError(f"Unknown architecture choice: {choice}")

    @staticmethod
    def create_backend(stack: BackendStack, project_name: str) -> BackendStrategy:
        backends = {
            BackendStack.JAVA: lambda: JavaSpringBackend(project_name),
            BackendStack.EXPRESS: lambda: ExpressBackend(),
            BackendStack.DJANGO: lambda: DjangoBackend(),
        }
        factory = backends.get(stack)
        if not factory:
            raise ValueError(f"Unknown backend stack: {stack}")
        return factory()

    @staticmethod
    def create_frontend(stack: FrontendStack) -> FrontendStrategy | None:
        if stack == FrontendStack.NONE:
            return None
        frontends = {
            FrontendStack.REACT: ReactFrontend,
            FrontendStack.LIT: LitFrontend,
            FrontendStack.ANGULAR: AngularFrontend,
        }
        cls = frontends.get(stack)
        if not cls:
            raise ValueError(f"Unknown frontend stack: {stack}")
        return cls()

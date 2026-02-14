import pytest

from skelly.core.models import BackendStack, FrontendStack
from skelly.factories.base import StrategyFactory
from skelly.factories.backend_factory import BackendFactory
from skelly.factories.frontend_factory import FrontendFactory
from skelly.strategies.architecture import (
    CustomArchitecture,
    HexagonalArchitecture,
    LayeredArchitecture,
)
from skelly.strategies.backend import DjangoBackend, ExpressBackend, JavaSpringBackend
from skelly.strategies.frontend import AngularFrontend, LitFrontend, ReactFrontend


class TestStrategyFactory:
    def test_create_hexagonal_architecture(self):
        strategy = StrategyFactory.create_architecture(
            "hexagonal", "myapp", BackendStack.EXPRESS
        )
        assert isinstance(strategy, HexagonalArchitecture)

    def test_create_hexagonal_java(self):
        strategy = StrategyFactory.create_architecture(
            "hexagonal", "myapp", BackendStack.JAVA
        )
        assert isinstance(strategy, HexagonalArchitecture)
        folders = strategy.get_folders()
        assert any("com/example" in f for f in folders)

    def test_create_layered_architecture(self):
        strategy = StrategyFactory.create_architecture(
            "layered", "myapp", BackendStack.EXPRESS
        )
        assert isinstance(strategy, LayeredArchitecture)

    def test_create_custom_architecture(self):
        strategy = StrategyFactory.create_architecture(
            "custom", "myapp", BackendStack.EXPRESS, ["src/foo"]
        )
        assert isinstance(strategy, CustomArchitecture)
        assert strategy.get_folders() == ["src/foo"]

    def test_create_unknown_architecture_raises(self):
        with pytest.raises(ValueError, match="Unknown architecture"):
            StrategyFactory.create_architecture(
                "unknown", "myapp", BackendStack.EXPRESS
            )

    def test_create_java_backend(self):
        strategy = StrategyFactory.create_backend(BackendStack.JAVA, "myapp")
        assert isinstance(strategy, JavaSpringBackend)

    def test_create_express_backend(self):
        strategy = StrategyFactory.create_backend(BackendStack.EXPRESS, "myapp")
        assert isinstance(strategy, ExpressBackend)

    def test_create_django_backend(self):
        strategy = StrategyFactory.create_backend(BackendStack.DJANGO, "myapp")
        assert isinstance(strategy, DjangoBackend)

    def test_create_react_frontend(self):
        strategy = StrategyFactory.create_frontend(FrontendStack.REACT)
        assert isinstance(strategy, ReactFrontend)

    def test_create_lit_frontend(self):
        strategy = StrategyFactory.create_frontend(FrontendStack.LIT)
        assert isinstance(strategy, LitFrontend)

    def test_create_angular_frontend(self):
        strategy = StrategyFactory.create_frontend(FrontendStack.ANGULAR)
        assert isinstance(strategy, AngularFrontend)

    def test_create_none_frontend(self):
        strategy = StrategyFactory.create_frontend(FrontendStack.NONE)
        assert strategy is None


class TestLibraryFactories:
    def test_backend_factory_java(self):
        libs = BackendFactory.get_supported_libraries(BackendStack.JAVA)
        assert len(libs) > 0
        values = [c.value for c in libs]
        assert "lombok" in values

    def test_backend_factory_express(self):
        libs = BackendFactory.get_supported_libraries(BackendStack.EXPRESS)
        assert len(libs) > 0
        values = [c.value for c in libs]
        assert "helmet" in values

    def test_backend_factory_django(self):
        libs = BackendFactory.get_supported_libraries(BackendStack.DJANGO)
        assert len(libs) > 0

    def test_frontend_factory_react(self):
        libs = FrontendFactory.get_supported_libraries(FrontendStack.REACT)
        assert len(libs) > 0

    def test_frontend_factory_none(self):
        libs = FrontendFactory.get_supported_libraries(FrontendStack.NONE)
        assert libs == []

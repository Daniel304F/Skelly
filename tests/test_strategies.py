from skelly.strategies.architecture import (
    CustomArchitecture,
    HexagonalArchitecture,
    LayeredArchitecture,
)
from skelly.strategies.backend import DjangoBackend, ExpressBackend, JavaSpringBackend
from skelly.strategies.frontend import AngularFrontend, LitFrontend, ReactFrontend


class TestArchitectureStrategies:
    def test_hexagonal_name(self):
        strategy = HexagonalArchitecture("myapp", "src")
        assert strategy.get_name() == "Hexagonal Architecture"

    def test_hexagonal_folders_express(self):
        strategy = HexagonalArchitecture("myapp", "src")
        folders = strategy.get_folders()
        assert "server/src/inbound/dto" in folders
        assert "server/src/domain/model" in folders
        assert "server/src/outbound/persistence" in folders
        assert "server/src/config" in folders

    def test_hexagonal_folders_java(self):
        strategy = HexagonalArchitecture("myapp", "java")
        folders = strategy.get_folders()
        assert any("com/example/myapp" in f for f in folders)

    def test_hexagonal_normalizes_name(self):
        strategy = HexagonalArchitecture("My App", "java")
        folders = strategy.get_folders()
        assert any("com/example/myapp" in f for f in folders)

    def test_layered_name(self):
        strategy = LayeredArchitecture()
        assert strategy.get_name() == "Layered Architecture"

    def test_layered_folders(self):
        strategy = LayeredArchitecture()
        folders = strategy.get_folders()
        assert "server/src/api/routes" in folders
        assert "server/src/services" in folders
        assert "server/src/models" in folders
        assert "server/src/repositories" in folders

    def test_custom_name(self):
        strategy = CustomArchitecture(["src/controllers"])
        assert strategy.get_name() == "Custom Architecture"

    def test_custom_folders(self):
        custom_folders = ["src/controllers", "src/models", "utils"]
        strategy = CustomArchitecture(custom_folders)
        assert strategy.get_folders() == custom_folders


class TestBackendStrategies:
    def test_java_spring_name(self):
        strategy = JavaSpringBackend("myapp")
        assert strategy.get_name() == "Java Spring Boot"

    def test_java_spring_folders(self):
        strategy = JavaSpringBackend("myapp")
        assert "server/src/main/resources" in strategy.get_folders()

    def test_java_spring_normalizes_name(self):
        strategy = JavaSpringBackend("My App")
        assert strategy.project_name == "myapp"
        assert strategy.base_package == "com.example.myapp"

    def test_express_name(self):
        strategy = ExpressBackend()
        assert strategy.get_name() == "Express.js"

    def test_express_folders(self):
        strategy = ExpressBackend()
        assert strategy.get_folders() == []

    def test_django_name(self):
        strategy = DjangoBackend()
        assert strategy.get_name() == "Django"

    def test_django_folders(self):
        strategy = DjangoBackend()
        assert strategy.get_folders() == []


class TestFrontendStrategies:
    def test_react_name(self):
        strategy = ReactFrontend()
        assert strategy.get_name() == "React"

    def test_react_folders(self):
        strategy = ReactFrontend()
        folders = strategy.get_folders()
        assert "frontend/src/components" in folders
        assert "frontend/src/pages" in folders

    def test_lit_name(self):
        strategy = LitFrontend()
        assert strategy.get_name() == "Lit"

    def test_lit_folders(self):
        strategy = LitFrontend()
        folders = strategy.get_folders()
        assert "frontend/src/components" in folders

    def test_angular_name(self):
        strategy = AngularFrontend()
        assert strategy.get_name() == "Angular"

    def test_angular_folders(self):
        strategy = AngularFrontend()
        folders = strategy.get_folders()
        assert "frontend/src/app/components" in folders
        assert "frontend/src/app/services" in folders

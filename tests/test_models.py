from skelly.core.models import (
    Architecture,
    BackendStack,
    FrontendStack,
    ProjectConfig,
)


class TestEnums:
    def test_frontend_stack_values(self):
        assert FrontendStack.REACT.value == "React"
        assert FrontendStack.LIT.value == "Lit"
        assert FrontendStack.ANGULAR.value == "Angular"
        assert FrontendStack.NONE.value == "None (Backend only)"

    def test_backend_stack_values(self):
        assert BackendStack.JAVA.value == "Java"
        assert BackendStack.EXPRESS.value == "Express"
        assert BackendStack.DJANGO.value == "Django"

    def test_architecture_values(self):
        assert Architecture.HEXAGONAL.value == "Hexagonal Architecture"
        assert Architecture.LAYERED.value == "Layered Architecture"
        assert Architecture.CUSTOM.value == "Custom Architecture"


class TestProjectConfig:
    def test_defaults(self):
        config = ProjectConfig(name="test", frontend_stack="React", backend_stack="Java")
        assert config.name == "test"
        assert config.architecture is None
        assert config.frontend_libraries == ()
        assert config.backend_libraries == ()
        assert config.output_path == "./"

    def test_with_all_fields(self):
        config = ProjectConfig(
            name="myapp",
            frontend_stack="React",
            backend_stack="Express",
            architecture="Hexagonal Architecture",
            frontend_libraries=("react-router-dom",),
            backend_libraries=("helmet", "cors"),
            output_path="/tmp",
        )
        assert config.name == "myapp"
        assert config.architecture == "Hexagonal Architecture"
        assert len(config.backend_libraries) == 2

    def test_frozen(self):
        config = ProjectConfig(name="test", frontend_stack="React", backend_stack="Java")
        import pytest
        with pytest.raises(AttributeError):
            config.name = "changed"

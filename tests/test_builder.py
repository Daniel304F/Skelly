import pytest

from skelly.core.builder import ProjectBuilder
from skelly.core.exceptions import BuildError
from skelly.strategies.architecture import LayeredArchitecture


class TestProjectBuilder:
    def test_fluent_api_returns_self(self):
        builder = ProjectBuilder()
        result = builder.set_meta_data("test")
        assert result is builder

    def test_set_meta_data_creates_config(self):
        builder = ProjectBuilder()
        builder.set_meta_data("myapp")
        assert builder.config is not None
        assert builder.config.name == "myapp"

    def test_chaining(self):
        builder = ProjectBuilder()
        builder.set_meta_data("test")\
               .set_frontend_stack("React")\
               .set_backend_stack("Express")\
               .set_architecture("Layered Architecture")\
               .add_frontend_libraries(["react-router-dom"])\
               .add_backend_libraries(["helmet"])
        assert builder.config.frontend_stack == "React"
        assert builder.config.backend_stack == "Express"
        assert builder.config.architecture == "Layered Architecture"
        assert "react-router-dom" in builder.config.frontend_libraries
        assert "helmet" in builder.config.backend_libraries

    def test_build_without_config_raises(self):
        builder = ProjectBuilder()
        with pytest.raises(BuildError, match="ProjectConfig is not initialized"):
            builder.build()

    def test_build_without_architecture_raises(self):
        builder = ProjectBuilder()
        builder.set_meta_data("test")
        with pytest.raises(BuildError, match="Architecture strategy is required"):
            builder.build()

    def test_build_creates_project(self, tmp_path):
        builder = ProjectBuilder()
        builder.set_meta_data("testproject")\
               .set_frontend_stack("None")\
               .set_backend_stack("Express")\
               .set_architecture("Layered Architecture")\
               .with_architecture_strategy(LayeredArchitecture())

        builder.config.output_path = str(tmp_path)
        config = builder.build()

        assert config.name == "testproject"
        project_dir = tmp_path / "testproject"
        assert project_dir.exists()
        assert (project_dir / "server/src/api/routes").exists()

    def test_with_frontend_strategy_accepts_none(self):
        builder = ProjectBuilder()
        result = builder.with_frontend_strategy(None)
        assert result is builder
        assert builder._frontend is None

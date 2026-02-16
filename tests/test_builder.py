import pytest

from skelly.core.builder import ProjectBuilder
from skelly.core.exceptions import BuildError
from skelly.strategies.architecture import LayeredArchitecture


class TestProjectBuilder:
    def test_fluent_api_returns_self(self):
        builder = ProjectBuilder()
        result = builder.set_meta_data("test")
        assert result is builder

    def test_chaining_stores_values(self):
        builder = ProjectBuilder()
        builder.set_meta_data("test")\
               .set_frontend_stack("React")\
               .set_backend_stack("Express")\
               .set_architecture("Layered Architecture")\
               .add_frontend_libraries(["react-router-dom"])\
               .add_backend_libraries(["helmet"])
        assert builder._frontend_stack == "React"
        assert builder._backend_stack == "Express"
        assert builder._architecture_name == "Layered Architecture"
        assert "react-router-dom" in builder._frontend_libraries
        assert "helmet" in builder._backend_libraries

    def test_build_without_name_raises(self):
        builder = ProjectBuilder()
        with pytest.raises(BuildError, match="Project name is not set"):
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

        # Override output path by setting the private field before build
        builder._output_path = str(tmp_path)
        config = builder.build()

        assert config.name == "testproject"
        project_dir = tmp_path / "testproject"
        assert project_dir.exists()
        assert (project_dir / "server/src/api/routes").exists()

    def test_build_creates_frozen_config(self):
        builder = ProjectBuilder()
        builder.set_meta_data("frozen_test")\
               .set_backend_stack("Express")\
               .set_architecture("Layered Architecture")\
               .add_backend_libraries(["helmet"])\
               .with_architecture_strategy(LayeredArchitecture())

        config = builder._create_config()

        assert config.name == "frozen_test"
        assert config.backend_libraries == ("helmet",)
        # frozen dataclass should not allow mutation
        with pytest.raises(AttributeError):
            config.name = "changed"

    def test_dry_run_does_not_create_files(self, tmp_path):
        builder = ProjectBuilder(dry_run=True)
        builder.set_meta_data("dryproject")\
               .set_frontend_stack("None")\
               .set_backend_stack("Express")\
               .set_architecture("Layered Architecture")\
               .with_architecture_strategy(LayeredArchitecture())

        config = builder.build()
        assert config.name == "dryproject"
        # No files should be created
        assert not (tmp_path / "dryproject").exists()

    def test_with_frontend_strategy_accepts_none(self):
        builder = ProjectBuilder()
        result = builder.with_frontend_strategy(None)
        assert result is builder
        assert builder._frontend is None

from skelly.core.template_renderer import render_template


class TestTemplateRenderer:
    def test_render_java_entity(self):
        result = render_template(
            "java_spring/hexagonal/domain/Example.java.j2",
            package="com.example.myapp",
        )
        assert "package com.example.myapp.domain.model;" in result
        assert "public class Example" in result
        assert "UUID" in result

    def test_render_pom_xml(self):
        deps = [
            {"group_id": "org.projectlombok", "artifact_id": "lombok", "version": "1.18.30"},
            {"group_id": "org.springframework.boot", "artifact_id": "spring-boot-starter-data-jpa", "version": None},
        ]
        result = render_template(
            "java_spring/pom.xml.j2",
            project_name="myapp",
            dependencies=deps,
        )
        assert "<artifactId>myapp</artifactId>" in result
        assert "<artifactId>lombok</artifactId>" in result
        assert "<version>1.18.30</version>" in result
        assert "spring-boot-starter-data-jpa" in result

    def test_render_pom_xml_no_deps(self):
        result = render_template(
            "java_spring/pom.xml.j2",
            project_name="empty",
            dependencies=[],
        )
        assert "<artifactId>empty</artifactId>" in result
        assert "spring-boot-starter-web" in result

    def test_render_express_controller(self):
        result = render_template(
            "express/hexagonal/adapter/ExampleController.js.j2",
        )
        assert "Router" in result
        assert "createExampleController" in result

    def test_render_express_index(self):
        result = render_template(
            "express/hexagonal/index.js.j2",
        )
        assert "express" in result
        assert "ExampleService" in result

    def test_render_application_properties(self):
        result = render_template(
            "java_spring/application.properties.j2",
            project_name="testapp",
        )
        assert "spring.application.name=testapp" in result
        assert "server.port=8080" in result

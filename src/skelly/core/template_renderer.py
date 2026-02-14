from pathlib import Path

from jinja2 import Environment, PackageLoader, select_autoescape


_env = Environment(
    loader=PackageLoader("skelly", "templates"),
    autoescape=select_autoescape([]),
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_template(template_path: str, **context: object) -> str:
    """Render a Jinja2 template with the given context variables."""
    template = _env.get_template(template_path)
    return template.render(**context)


def render_to_file(template_path: str, output_path: Path, **context: object) -> None:
    """Render a Jinja2 template and write the result to a file."""
    content = render_template(template_path, **context)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(content)

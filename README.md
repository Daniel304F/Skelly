# Skelly

A smart scaffolding CLI that generates modular full-stack project structures. Choose your frontend, backend, and architecture pattern — Skelly handles the rest.

## Features

- **Interactive CLI** — guided prompts for project name, stacks, libraries, and architecture
- **Multiple backends** — Java Spring Boot, Express.js, Django
- **Multiple frontends** — React, Lit, Angular (or backend-only)
- **Architecture patterns** — Hexagonal (Ports & Adapters), Layered, or Custom
- **Dry-run mode** — preview the folder structure without creating any files
- **Jinja2 templates** — generated boilerplate code (controllers, services, entities) for hexagonal setups
- **Library selection** — pick common libraries per stack during scaffolding

## Installation

Requires Python 3.10+.

```bash
pip install -e .
```

For development (includes pytest):

```bash
pip install -e ".[dev]"
```

## Usage

```bash
skelly
```

The CLI will prompt you for:
1. Project name
2. Frontend stack (React, Lit, Angular, or None)
3. Backend stack (Java, Express, Django)
4. Libraries for each stack
5. Architecture pattern (Hexagonal, Layered, Custom)

### Dry-run mode

Preview what would be created without writing any files:

```bash
skelly --dry-run
```

## Project Structure

```
skelly/
├── src/
│   └── skelly/
│       ├── cli.py                  # CLI entry point (questionary + argparse)
│       │
│       ├── core/
│       │   ├── models.py           # Enums (FrontendStack, BackendStack, Architecture) & frozen ProjectConfig
│       │   ├── builder.py          # Builder pattern — orchestrates strategies, creates config
│       │   ├── exceptions.py       # SkellyError, BuildError, DependencyInstallError, TemplateRenderError
│       │   └── template_renderer.py # Jinja2 wrapper (render_template, render_to_file)
│       │
│       ├── factories/
│       │   ├── base.py             # StrategyFactory — creates architecture/backend/frontend strategies
│       │   ├── backend_factory.py  # Library choices per backend stack
│       │   └── frontend_factory.py # Library choices per frontend stack
│       │
│       ├── strategies/
│       │   ├── base.py             # ABC interfaces (ArchitectureStrategy, BackendStrategy, FrontendStrategy)
│       │   ├── architecture/       # Hexagonal, Layered, Custom
│       │   ├── backend/            # Express, Java Spring, Django
│       │   └── frontend/           # React, Lit, Angular
│       │
│       └── templates/              # Jinja2 code templates (.j2)
│           ├── express/hexagonal/  # Express.js hexagonal boilerplate
│           └── java_spring/        # Spring Boot hexagonal boilerplate + pom.xml
│
├── tests/                          # pytest test suite
│   ├── test_builder.py
│   ├── test_models.py
│   ├── test_factories.py
│   ├── test_strategies.py
│   └── test_templates.py
│
└── pyproject.toml
```

## Design Patterns

- **Builder** — `ProjectBuilder` collects configuration via a fluent API, then creates an immutable `ProjectConfig` at build time
- **Strategy** — swappable architecture, backend, and frontend strategies behind abstract interfaces
- **Factory** — `StrategyFactory` maps user choices to concrete strategy instances

## Running Tests

```bash
pytest
```

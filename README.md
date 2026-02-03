# Skelly

A smart scaffolding CLI that generates modular project structures. Choose your frontend and backend with ease.

## Projektstruktur

```
skelly/
├── src/
│ └── skelly/
│ ├── **init**.py
│ ├── **main**.py #'python -m skelly'
│ ├── cli.py # Questionary-Logik & User-Interaktion
│ │
│ ├── core/ # Gemeinsame Modelle & Logik
│ │ ├── models.py # ProjectConfig (Name, Stack, Architektur)
│ │ └── builder.py # Das Builder-Pattern (dirigiert den Bau)
│ │
│ ├── factories/ # Abstract Factory Pattern
│ │ ├── base.py # Interface für ProjectFactory
│ │ ├── backend_factory.py
│ │ └── frontend_factory.py
│ │
│ ├── strategies/ # Strategy Pattern for different software architectures
│ │ ├── base.py # Interface für Architekturen
│ │ ├── hexagonal.py # Logik für Ports & Adapters
│ │ └── standard.py
│ │
│ └── templates/ # Rohdateien/Blueprints (.txt, .java, .ts)
│ ├── backend/
│ └── frontend/
│
├── tests/ # Unit- & Integrationtests
└── pyproject.toml
```

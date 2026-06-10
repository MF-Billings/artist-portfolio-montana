# Project Rules & Standards

## 1. Development Philosophy
- **TDD (Test Driven Development)** is mandatory.
    - **RED**: Write a failing test for the feature/bug.
    - **GREEN**: Write the minimal code to pass the test.
    - **REFACTOR**: Improve code quality while keeping tests green.
- **MVP Logic**: Do not over-engineer. Stick to the simplest solution that satisfies the requirement (e.g., SQLite, Simple Views).
- **Modularity**: Code should be split into small, modular chunks. Avoid monolithic functions or classes.

## 2. Directory Structure
We use a separate `apps` directory to keep the root clean.
```text
artist_portfolio_montana/
├── apps/
│   ├── core/         # General views (Home, About, Contact)
│   └── portfolio/    # Logic for Artworks, Tags, Galleries
├── config/           # Django Project Settings (formerly 'artist_portfolio')
├── static/           # Global static files (SCSS, JS, Images)
├── templates/        # Global templates (base.html)
├── manage.py
├── AGENTS.md
├── pyproject.toml
└── uv.lock
```

## 3. Tech Stack Specifics
- **Database**: SQLite (Dev), Postgres (Prod).
- **Containerization**: Docker + Docker Compose.
- **Tagging**: `django-treebeard` (Materialized Path implementation).
- **CSS**: `Pico.css` (SCSS version).
    - All customizations must happen in `static/scss/style.scss`.
    - Do not write inline styles unless absolutely necessary.
    - Use `django-compressor` and `django-libsass` for compilation.

## 4. Testing Guidelines
- Use `pytest` as the runner.
- Use `factory_boy` for creating test data.
- Test files should mirror the app structure (e.g., `apps/portfolio/tests/test_models.py`).

## 5. Coding Style
- **Formatter**: `black`
- **Linter**: `flake8`
- Follow PEP 8 guidelines.

## 6. Documentation Guidelines
- **Keep Documentation Updated**: All documentation (such as README files, execution plans, and API docs) must always be updated to reflect code changes.
- **Document All Commands**: No command (e.g., new management commands, runner options, setup scripts) should be left undocumented.

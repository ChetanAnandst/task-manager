# Integration Plan

## Backend
- Project folder: `task-manager/`
- Framework: Django 5.x, CPython 3.12
- Run command: `docker compose up --build`
- Local port: `8000`
- Build command: `docker compose build`
- Health endpoint: `GET /health`

## Frontend
- Server-rendered Django templates; no separate frontend framework.
- Template entry: `templates/base.html`
- Task views: `tasks/templates/tasks/task_list.html`, `tasks/templates/tasks/task_form.html`
- Static CSS: `static/css/app.css`
- API seam: none. Server-rendered task calls use Django views and forms.
- Mock files: none.

## API routes
- `GET /health`
- `GET /`
- `GET /tasks/new`
- `POST /tasks/new`
- `GET /tasks/<id>/edit`
- `POST /tasks/<id>/edit`
- `POST /tasks/<id>/complete`
- `POST /tasks/<id>/delete`
- `GET|POST /accounts/signup`
- `GET|POST /accounts/login`
- `POST /accounts/logout`

## Database
- Type: SQLite
- Migration tool: Django migrations
- Migration directory: `tasks/migrations/`
- Connection env: `DATABASE_PATH`
- Docker default: `/app/data/tasks.sqlite3`
- Explicit requirement: migrations only; do **not** create seed data.

## Shared types
- Django models and templates share `tasks/models.py`; no separate typed-client package.

## Services
- Essential: Django web service, SQLite persistent Docker volume.
- Enhancement: none. No cloud provider or Azure services selected.

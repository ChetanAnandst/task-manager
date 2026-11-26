# Project Plan

**Status**: Approved
**Created**: 2026-11-26
**Mode**: NEW

---

## 1. Project Overview

**Goal**: Build a separate, portfolio-ready task manager in the `task-manager` sibling folder, using simple server-rendered Python pages, SQLite, local Docker first, and a cloud provider chosen later. Guest tasks remain private to the current browser; signing in enables cross-device access. The project is designed so that every module is independently testable.

**App Type**: Full-stack SSR

**API Login**: Yes

**Mode**: NEW

**Deployment Plan**: No deployment plan found

---

## 2. Backend - Django

| Component | Technology |
|-----------|-----------|
| **Language** | Python |
| **Runtime** | CPython |
| **Framework** | Django |
| **Package Manager** | pip |
| **Test Runner** | pytest |
| **Mocking Library** | unittest.mock |
| **Test Command** | `python -m pytest` |
| **Orchestration** | docker-compose |

---

## 3. Services Required

| Azure Service | Role in App | Environment Variable | Default Value (Local) | Classification |
|---------------|------------|---------------------|----------------------|----------------|
| SQLite (local; not an Azure service) | Essential embedded store for tasks, account data, and browser-scoped guest tasks | `DATABASE_PATH` | `/app/data/tasks.sqlite3` on a persistent Docker volume | Essential |

---

No Azure cloud services are selected for the initial phase; the target is local Docker, and the cloud provider remains undecided.

## 4. Prerequisites

Verify any ❓ entries before local setup. The selected local runtime is Docker (as requested); the Docker CLI and Compose are present, but the Docker engine was not reachable during this scan. Python was not confirmed on the host. A container image can package the Python runtime, but Docker must be running to use the planned local container workflow.

### Run

| Tool | Service(s) | Installed | Version |
|------|------------|-----------|---------|
| Python / CPython 3.12 target | web | ❓ | No compatible host interpreter confirmed; project target is CPython 3.12 |
| pip | web | ❓ | Not confirmed because no host Python interpreter was found |

### Debug

| Tool | Service(s) | Installed | Version |
|------|------------|-----------|---------|
| Docker | web | ❓ | Docker CLI 29.9.3 found; Linux engine/daemon unreachable |
| Docker Compose | web | ✅ | v5.7.0 |
| `ms-python.python` VS Code extension | web | ✅ | 2026.10.0 |
| `ms-python.debugpy` VS Code extension | web | ✅ | 2026.6.0 |

---

## 5. Project Structure

```text
task-manager/
├── .azure/
│   ├── requirements.json
│   └── project-plan.md
├── .env.example
├── .gitignore
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── manage.py
├── taskmanager/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── tasks/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── templates/
│       └── tasks/
│           ├── task_list.html
│           ├── task_form.html
│           └── task_confirm_delete.html
├── templates/
│   ├── base.html
│   └── registration/
│       ├── login.html
│       └── signup.html
└── data/                         # Persistent SQLite volume mount; generated at runtime
```

Django templates render the pages on the server. Guest task records are scoped to the current browser session and are not synchronized across devices; signed-in task records are available across devices. The initial local Docker deployment uses SQLite and does not provision cloud resources.

---

## 6. Route Definitions

| # | Method | Path | Description | Request Body | Response Body | Status Codes |
|---|--------|------|-------------|-------------|--------------|-------------|
| 1 | GET | `/health` | Container/app health check | — | `healthy` | 200, 503 |
| 2 | GET | `/` | Render current browser's or signed-in user's task list | Query filters: status, priority, due date | HTML task list | 200 |
| 3 | GET | `/tasks/new` | Render task creation form | — | HTML form | 200 |
| 4 | POST | `/tasks/new` | Create a task | title, description, due date, priority | Redirect to task list | 303, 400 |
| 5 | GET | `/tasks/<id>/edit` | Render task edit form | — | HTML form | 200, 404 |
| 6 | POST | `/tasks/<id>/edit` | Update a task | editable task fields | Redirect to task list | 303, 400, 404 |
| 7 | POST | `/tasks/<id>/complete` | Mark a task complete or reopen it | completion state | Redirect to task list | 303, 404 |
| 8 | POST | `/tasks/<id>/delete` | Delete a task | — | Redirect to task list | 303, 404 |
| 9 | GET/POST | `/accounts/signup` | Render and submit account creation form | account form fields | HTML form or redirect | 200, 303, 400 |
| 10 | GET/POST | `/accounts/login` | Render and submit sign-in form | account form fields | HTML form or redirect | 200, 303, 400 |
| 11 | POST | `/accounts/logout` | Sign out | — | Redirect to task list | 303 |

---

## 7. Next Steps

1. Review and explicitly approve this plan before scaffolding.
2. Run **azure-project-scaffold** to execute the approved plan.
3. Run **azure-project-integrate** to smoke-test the backend and verify the database schema and live task flows.
4. Run **azure-debug-plan** → **azure-debug-generate** for Docker and VS Code debugging.
5. Choose a cloud provider later, then run the **azure-deploy** agent when ready.

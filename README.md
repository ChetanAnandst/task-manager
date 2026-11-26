# Task Manager

A local-first Django task manager with server-rendered pages and SQLite.

## Run with Docker Compose

Docker Desktop or another Docker engine must be running.

```text
docker compose up --build
```

Open http://localhost:8000. The SQLite database is stored in the `task-data` Docker volume.

## Local Python

The intended target is CPython 3.12.

```text
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python -m pytest
```

Guest tasks belong only to the current browser session. Signing in creates or identifies an account and moves that browser's guest tasks into the account.

## Continuous integration

GitHub Actions runs Django checks and tests, then builds the Docker image for every push and pull request. The workflow does not publish an image or deploy to a cloud provider; those can be added when you choose a hosting target.

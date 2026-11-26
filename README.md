# Task Manager

A local-first Django task manager with server-rendered pages and SQLite.

## Run with Docker Compose

Docker Desktop or another Docker engine must be running.

```text
docker compose up --build
```

Open http://localhost:8000. The SQLite database is stored in the `task-data` Docker volume.

### Open it on a phone on the same Wi-Fi or hotspot

On the PC, run `ipconfig` and find the IPv4 address of the Wi-Fi adapter connected to the same network as the phone. Copy `.env.example` to `.env`, then add that address to `DJANGO_ALLOWED_HOSTS`, separated by a comma. For example:

```text
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,10.0.0.25
```

Restart with `docker compose up --build`, then open `http://<PC-IPv4-address>:8000` on the phone. Do not use `localhost` on the phone; that refers to the phone itself. Both devices must be able to communicate on the same local network.

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

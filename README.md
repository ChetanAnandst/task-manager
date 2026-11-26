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

## How the project works

The request path is:

```text
Browser
  -> host port 8000
  -> Docker Compose web container
  -> Gunicorn (WSGI server)
  -> Django middleware and URL routing
  -> task view and Django ORM
  -> SQLite database in the task-data volume
  -> rendered Django template returned to the browser
```

CSS and JavaScript are collected into `staticfiles/` during the image build. WhiteNoise serves these files from the same web container, so a separate web server is not required for this local project.

### Main components and why they are used

| Component | Purpose in this project |
| --- | --- |
| Python 3.12 | Runtime for the Django application. |
| Django | URL routing, request handling, forms, authentication, sessions, ORM, templates, and CSRF protection. |
| Django templates | Render task pages on the server; this is not a React or single-page application. |
| SQLite | Simple local database that needs no separate database service. |
| Dockerfile | Defines how to install dependencies, collect static files, and start the application image. |
| Docker Compose | Builds and runs the web service, publishes port 8000, provides environment settings, and mounts persistent data. |
| Gunicorn | Runs Django's WSGI application inside the container. |
| WhiteNoise | Serves collected CSS and JavaScript through the Django application container. |
| pytest and pytest-django | Run the application tests, including guest privacy and task ownership checks. |
| GitHub Actions | Runs checks/tests and builds the image on pushes and pull requests; it does not deploy the site. |
| Browser JavaScript and localStorage | Toggle light/dark mode and remember the choice in that browser. |

### Task and account flow

- `tasks/models.py` defines task title, description, due date, priority, completion state, optional account owner, guest-session key, and timestamps.
- `tasks/forms.py` uses a Django `ModelForm` to validate and save task input.
- `tasks/urls.py` maps list, create, edit, complete, delete, signup, login, and health-check URLs to views.
- `tasks/views.py` scopes every task query to the signed-in owner or the current guest session. Complete and delete operations require POST requests.
- A guest gets a random key stored in their Django session. Guest tasks are private to that browser session; they do not automatically sync to another device.
- Signing up or signing in moves that browser session's guest tasks to the account, so the user can then access them after logging in on another device.
- Django templates under `templates/` and `tasks/templates/` render the pages. `static/css/app.css` styles them, and `static/js/theme.js` handles the theme control.

## Docker concepts used here

- **Image:** The built application package produced by `Dockerfile`.
- **Container:** A running instance of that image. Application code and its Python dependencies run inside it.
- **Compose service:** The `web` configuration in `compose.yaml` that tells Docker how to build and run the container.
- **Port mapping:** `8000:8000` maps port 8000 on the PC to port 8000 in the container. Gunicorn binds to `0.0.0.0:8000` inside the container.
- **Named volume:** `task-data` stores `/app/data/tasks.sqlite3` outside the disposable container. Recreating the container keeps the database.
- **Static collection:** `collectstatic` copies app and Django static files into `staticfiles/` while building the image; WhiteNoise serves them at `/static/`.

Useful commands:

```powershell
docker compose up --build
docker compose ps
docker compose logs -f web
docker compose exec web python manage.py check
docker compose exec web python -m pytest
docker compose down
```

`docker compose down` stops/removes the containers but keeps the named database volume. Avoid `docker compose down -v` unless you intend to delete that volume and its task data.

## Troubleshooting approach

Start with the exact URL, error message, and whether the problem happens on the PC, phone, or both. Then check one layer at a time:

Use this loop rather than changing several things at once:

1. State the expected result and the actual result.
2. Find the boundary: browser, network, Docker port/container, Django, database, or template/static files.
3. Gather evidence at that boundary, such as the browser error, HTTP response, `docker compose ps`, or container logs.
4. Make one testable hypothesis and run the smallest check that can confirm or reject it.
5. Apply one focused fix, repeat the original failing action, then run the relevant tests.

1. **Is the container running?** Run `docker compose ps`; inspect `docker compose logs -f web` for startup or migration errors.
2. **Is the port published?** Confirm the service shows `8000->8000`. On the PC, use `http://localhost:8000`.
3. **Is it a phone/network issue?** On the phone, use `http://<PC-IPv4-address>:8000`, not `localhost`. The phone and PC must be able to reach each other on the same Wi-Fi/hotspot; firewall rules or hotspot isolation can block this.
4. **Is Django rejecting the host?** A `DisallowedHost` page means the address is missing from `DJANGO_ALLOWED_HOSTS`. Add the PC's current IPv4 address to `.env`, then recreate the service with `docker compose up -d`.
5. **Is the page unstyled?** Check that `/static/css/app.css` and `/static/js/theme.js` load. The image build runs `collectstatic`, and WhiteNoise serves the collected files.
6. **Is there a Django error page or HTTP 500?** Read the web service logs before changing code. Run `python manage.py check` and the tests to narrow down configuration versus application errors.
7. **Did tasks disappear after a container rebuild?** Check that Compose still mounts `task-data` at `/app/data`. The named volume should persist across normal container rebuilds.

Common symptoms:

| Symptom | First likely cause to check |
| --- | --- |
| `ERR_CONNECTION_REFUSED` | App/container stopped, wrong port, or port not published. |
| `DisallowedHost` | Request host is not listed in `DJANGO_ALLOWED_HOSTS`. |
| Unstyled HTML | Static files were not collected or are not being served. |
| Works on PC but not phone | Phone used `localhost`, devices cannot reach each other, firewall blocks port 8000, or hotspot isolation is enabled. |
| Task missing on another device | Guest tasks belong to one browser session; sign in on both devices to use account tasks. |
| HTTP 500 | Inspect container logs and reproduce with the smallest failing request. |

This Compose setup is for local development and trusted local-network testing, not public internet hosting. It enables Django debug mode and uses a development secret. Public deployment needs production settings, a real secret, HTTPS, an appropriate database and backup plan, and a hosting provider.

## Interview preparation

### Short project explanation

> I built Taskboard as a local-first task manager using Django. It supports task creation, editing, completion, deletion, due dates, priorities, and filtering. Guests can use it privately in one browser session, and signing in moves those guest tasks to the user's account. Django renders the pages and uses SQLite for data. Docker Compose makes the app easy to run, a named volume preserves the database, Gunicorn runs Django, and WhiteNoise serves the collected frontend assets. The tests cover guest privacy, task ownership, and the health endpoint.

### Questions you should be ready for

1. **What problem does the app solve?**

   It gives a user a simple place to track tasks and lets a guest start without creating an account. Accounts allow tasks to follow the user across browsers after sign-in.

2. **How does a request reach the database and back?**

   The browser sends an HTTP request to the published port. Gunicorn passes it to Django; middleware and URL routing select a view; the view validates input and uses the ORM; the view renders a template and Django returns the response.

3. **How are guest tasks kept private?**

   Django creates a random guest key in the browser's session. Queries for anonymous users filter by that key, while signed-in users query by account owner. The tests verify a second client cannot see the first client's guest task.

4. **How do you prevent a user editing another user's task?**

   The view first looks up the task through `visible_tasks(request)`, which is already scoped to that user or guest session. A task outside that scope returns 404.

5. **Why use SQLite? What would change at larger scale?**

   SQLite is lightweight and keeps local setup simple. For concurrent production use, I would evaluate PostgreSQL, configure backups and migrations, and test the deployment and data migration plan.

6. **Why Docker and Compose?**

   Docker packages the app runtime and dependencies. Compose makes the web service, port, environment, and persistent database volume reproducible with one command.

7. **What is the difference between an image and a container?**

   The image is the built template; a container is a running instance of it. The SQLite volume is separate so data survives container replacement.

8. **Why Gunicorn and WhiteNoise?**

   Gunicorn runs Django through WSGI. WhiteNoise lets this small deployment serve collected CSS and JavaScript without adding another web-server service.

9. **How do you test it?**

   `python -m pytest` runs the tests. Current tests check guest-session privacy, task ownership, and the health endpoint. I would add tests for create/edit/delete, filters, authentication task transfer, and static delivery as those areas change.

10. **How would you investigate a phone connection failure?**

    Separate browser, network, Docker port, and Django host validation. Check the URL and PC IPv4, container status and port mapping, then distinguish a connection refusal from a Django `DisallowedHost` response.

11. **Is it publicly deployed?**

    No. GitHub Actions tests and builds the image but does not publish or deploy it. A phone can reach it only when the local network permits it; public access needs hosting and production configuration.

12. **What would you improve next?**

    Good examples are stronger production settings, PostgreSQL and backups for hosted use, pagination, more view/form tests, accessible UI checks, and a deployment pipeline after choosing a hosting provider.

## Questions to ask while learning the code

- What is the input, output, and side effect of this view?
- Which URL calls it, and which template does it render?
- Which database query runs, and how is it scoped to a user or guest?
- What should happen for invalid form data or an unauthorized task ID?
- Which test would fail if this behavior regressed?
- Is this configuration for the browser, Django, Docker build time, or container runtime?
- If the app fails, what is the first observable fact I can check before changing code?

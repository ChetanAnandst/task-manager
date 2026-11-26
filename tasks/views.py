import uuid
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TaskForm
from .models import Task


def guest_key(request):
    key = request.session.get("guest_key")
    if not key:
        key = uuid.uuid4().hex
        request.session["guest_key"] = key
    return key


def visible_tasks(request):
    if request.user.is_authenticated:
        return Task.objects.filter(owner=request.user)
    return Task.objects.filter(owner__isnull=True, guest_key=guest_key(request))


def health(request):
    try:
        connection.ensure_connection()
        return HttpResponse("healthy", content_type="text/plain")
    except Exception:
        return HttpResponse("unhealthy", status=503, content_type="text/plain")


def task_list(request):
    tasks = visible_tasks(request)
    status = request.GET.get("status")
    priority = request.GET.get("priority")
    due = request.GET.get("due")
    if status == "open":
        tasks = tasks.filter(completed=False)
    elif status == "complete":
        tasks = tasks.filter(completed=True)
    if priority:
        tasks = tasks.filter(priority=priority)
    if due == "today":
        from django.utils import timezone
        tasks = tasks.filter(due_date=timezone.localdate())
    elif due == "overdue":
        from django.utils import timezone
        tasks = tasks.filter(due_date__lt=timezone.localdate(), completed=False)
    return render(request, "tasks/task_list.html", {"tasks": tasks})


def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            if request.user.is_authenticated:
                task.owner = request.user
            else:
                task.guest_key = guest_key(request)
            task.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form": form})


def task_edit(request, task_id):
    task = get_object_or_404(visible_tasks(request), pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "tasks/task_form.html", {"form": form, "task": task})


@require_POST
def task_complete(request, task_id):
    task = get_object_or_404(visible_tasks(request), pk=task_id)
    task.completed = not task.completed
    task.save(update_fields=["completed", "updated_at"])
    return redirect("task_list")


@require_POST
def task_delete(request, task_id):
    task = get_object_or_404(visible_tasks(request), pk=task_id)
    task.delete()
    return redirect("task_list")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            key = guest_key(request)
            user = form.save()
            Task.objects.filter(owner__isnull=True, guest_key=key).update(owner=user, guest_key="")
            login(request, user)
            return redirect("task_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            key = guest_key(request)
            user = form.get_user()
            login(request, user)
            Task.objects.filter(owner__isnull=True, guest_key=key).update(owner=user, guest_key="")
            return redirect("task_list")
    else:
        form = AuthenticationForm(request)
    return render(request, "registration/login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    return redirect("task_list")

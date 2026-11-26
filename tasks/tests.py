from django.contrib.auth.models import User
from django.test import TestCase

from .models import Task


class GuestTaskTests(TestCase):
    def test_guest_tasks_are_private_to_session(self):
        first = self.client
        response = first.post("/tasks/new", {"title": "Private task", "description": "", "due_date": "", "priority": "medium"})
        self.assertEqual(response.status_code, 302)
        self.assertContains(first.get("/"), "Private task")

        second = self.client_class()
        self.assertNotContains(second.get("/"), "Private task")

    def test_user_cannot_edit_another_users_task(self):
        owner = User.objects.create_user("owner", password="strong-pass-123")
        other = User.objects.create_user("other", password="strong-pass-123")
        task = Task.objects.create(title="Mine", owner=owner)
        self.client.login(username="other", password="strong-pass-123")
        response = self.client.post(f"/tasks/{task.id}/edit", {"title": "Changed", "description": "", "due_date": "", "priority": "medium"})
        self.assertEqual(response.status_code, 404)


class HealthTest(TestCase):
    def test_health_returns_healthy(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"healthy")

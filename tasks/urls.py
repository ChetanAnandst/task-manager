from django.urls import path
from . import views

urlpatterns = [
    path("health", views.health, name="health"),
    path("", views.task_list, name="task_list"),
    path("tasks/new", views.task_create, name="task_create"),
    path("tasks/<int:task_id>/edit", views.task_edit, name="task_edit"),
    path("tasks/<int:task_id>/complete", views.task_complete, name="task_complete"),
    path("tasks/<int:task_id>/delete", views.task_delete, name="task_delete"),
    path("accounts/signup", views.signup, name="signup"),
    path("accounts/login", views.login_view, name="login"),
    path("accounts/logout", views.logout_view, name="logout"),
]

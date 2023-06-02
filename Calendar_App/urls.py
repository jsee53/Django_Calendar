from django.urls import path
from . import views

urlpatterns = [
    path("", views.main),
    path("main", views.main),
    path("login", views.login),
    path("signup", views.signup),
    path("schedule", views.schedule),
    path("addpost", views.addpost),
]
from django.urls import path
from . import views

urlpatterns = [
    path("calendar", views.calendar),
    path("login", views.login),
    path("signup", views.signup),
    path("schedule", views.schedule),
    path("addpost", views.addpost),
]
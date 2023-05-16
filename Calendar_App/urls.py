from django.urls import path
from . import views

urlpatterns = [
    path("", views.main),
    path("submit_data", views.submit_data),
]
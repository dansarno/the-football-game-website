from django.urls import path
from . import views

app_name = "enter"
urlpatterns = [
    path("", views.index, name="index"),
    path("confirm", views.confirm, name="confirm")
]

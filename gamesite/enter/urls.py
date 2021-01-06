from django.urls import path
from . import views

app_name = "enter"
urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<int:entry_id>", views.edit_entry, name="entry"),
    path("entry/new", views.create_entry, name="create_entry"),
    path("entry/delete/<int:entry_id>", views.delete_entry, name="delete_entry"),
    path("confirm", views.confirm, name="confirm")
]

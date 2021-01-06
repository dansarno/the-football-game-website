from django.urls import path
from . import views

app_name = "enter"
urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<int:entry_id>", views.edit_entry, name="entry"),
    path("entry/new", views.new_entry, name="new_entry"),
    path("confirm", views.confirm, name="confirm")
]

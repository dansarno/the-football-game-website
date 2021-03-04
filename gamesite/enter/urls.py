from django.urls import path
from . import views
from .api.views import entries_detail

app_name = "enter"
urlpatterns = [
    path("entrymanager", views.index, name="index"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("results", views.results, name="results"),
    path("entry/<int:entry_id>", views.edit_entry, name="entry"),
    path("entry/new", views.create_entry, name="create_entry"),
    path("entry/random", views.create_random_entry, name="create_random_entry"),
    path("entry/delete/<int:entry_id>", views.delete_entry, name="delete_entry"),
    path("entry/submit/<int:entry_id>", views.submit_entry, name="submit_entry"),
    path("confirm", views.confirm, name="confirm"),
    path('api/all', entries_detail, name='all_entries_api'),
]

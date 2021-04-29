from django.urls import path
from . import views
from .api.views import teams_detail, entries_detail, my_entries_detail, called_bet_stats, called_bet_position_changes

app_name = "enter"
urlpatterns = [
    path("entrymanager", views.index, name="index"),
    path("leaderboard", views.leaderboard, name="leaderboard"),
    path("results", views.results, name="results"),
    path("explore", views.explore, name="explore"),
    path("entry/<int:entry_id>", views.edit_entry, name="entry"),
    path("entry/new", views.create_entry, name="create_entry"),
    path("entry/random", views.create_random_entry, name="create_random_entry"),
    path("entry/delete/<int:entry_id>", views.delete_entry, name="delete_entry"),
    path("entry/submit/<int:entry_id>", views.submit_entry, name="submit_entry"),
    path("entry/view/<int:entry_id>", views.view_entry, name="view_entry"),
    path('api/all', entries_detail, name='all_entries_api'),
    path('api/me', my_entries_detail, name='my_entries_api'),
    path('api/teams', teams_detail, name='teams_api'),
    path('api/called-bet-stats/<int:called_bet_id>',
         called_bet_stats, name='bet_success_api'),
    path('api/called-bet-changes/<int:called_bet_id>',
         called_bet_position_changes, name='bet_changes_api'),
]

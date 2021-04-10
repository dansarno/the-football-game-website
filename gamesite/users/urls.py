from django.urls import path
from django.conf.urls import url
from .views import profile, profile_edit
from .api.views import profile_history, profile_performance, winning_positions

# app_name = "users"
urlpatterns = [
    path('<str:username>', profile, name='profile'),
    path('<str:username>/api/history',
         profile_history, name='profile_history_api'),
    path('<str:username>/api/performance',
         profile_performance, name='profile_performance_api'),
    path('prize-api/', winning_positions, name='prize_api'),
    path('edit', profile_edit, name='profile_edit'),
]

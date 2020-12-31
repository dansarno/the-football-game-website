from django.urls import path
from .views import profile, profile_edit

# app_name = "users"
urlpatterns = [
    path('<str:username>', profile, name='profile'),
    path('edit', profile_edit, name='profile_edit'),
]

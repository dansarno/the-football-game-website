from django.urls import path
from django.conf.urls import url
from .views import profile, profile_edit
from .api.views import ProfileDataView, profile_detail

# app_name = "users"
urlpatterns = [
    path('<str:username>', profile, name='profile'),
    path('<str:username>/api/', profile_detail, name='profile_api'),
    path('edit', profile_edit, name='profile_edit'),
]

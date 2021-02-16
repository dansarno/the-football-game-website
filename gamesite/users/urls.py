from django.urls import path
from django.conf.urls import url
from .views import profile, profile_edit, get_data, ChartData

# app_name = "users"
urlpatterns = [
    path('<str:username>', profile, name='profile'),
    url(r'^api/$', get_data, name='api'),
    url(r'^api/chart/$', ChartData.as_view()),
    path('edit', profile_edit, name='profile_edit'),
]

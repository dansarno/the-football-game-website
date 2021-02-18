from django.urls import path
from .views import PostListView, PostDetailView, PostDeleteView, PostUpdateView, landing, feed
from . import views

app_name = "feed"
urlpatterns = [
    path("", landing, name="landing"),
    path("home", feed, name="home"),
    # path("home", PostListView.as_view(), name="home"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="delete"),
]

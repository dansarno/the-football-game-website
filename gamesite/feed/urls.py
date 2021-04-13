from django.urls import path
from .views import PostListView, PostDetailView, PostDeleteView, PostUpdateView, landing, charity, how_it_works, about
from . import views

app_name = "feed"
urlpatterns = [
    path("", landing, name="landing"),
    path("charity/", charity, name="charity"),
    path("how-it-works/", how_it_works, name="how-it-works"),
    path("about/", about, name="about"),
    path("home/", PostListView.as_view(), name="home"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="delete"),
]

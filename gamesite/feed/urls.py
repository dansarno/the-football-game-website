from django.urls import path
from .views import PostListView, PostDetailView, PostDeleteView, PostUpdateView, landing, charity, how_it_works, about, entry_guide, entry_guide_italian, how_it_works_italian, glossary, export_csv
from . import views

app_name = "feed"
urlpatterns = [
    path("", landing, name="landing"),
    path("glossario/", glossary, name="glossary"),
    path("entry-guide/", entry_guide, name="entry-guide"),
    path("guida/", entry_guide_italian, name="entry-guide-IT"),
    path("charity/", charity, name="charity"),
    path("how-it-works/", how_it_works, name="how-it-works"),
    path("come-funziona/", how_it_works_italian, name="how-it-works-IT"),
    path("about/", about, name="about"),
    path("export/", export_csv),
    path("home/", PostListView.as_view(), name="home"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="delete"),
]

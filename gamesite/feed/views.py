from django.shortcuts import render
from .models import Post


def home(request, template_name="feed/home.html"):
    posts = Post.objects.all()
    return render(request, template_name, {
        'title': "Home",
        'posts': posts
    })

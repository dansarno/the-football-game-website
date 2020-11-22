from django.http import HttpResponse
from django.shortcuts import render

games = ["foo", "bar", "baz"]


def index(request):
    return render(request, "enter/index.html", {
        "games": games
    })

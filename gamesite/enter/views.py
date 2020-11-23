from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

games = ["foo", "bar", "baz"]
CHOICES = [("home", "Home"), ("draw", "Draw"), ("away", "Away")]
submissions = []


class GroupGamesForm(forms.Form):
    game1 = forms.ChoiceField(choices=CHOICES, required=True, widget=forms.RadioSelect, label="Italy vs England")
    game2 = forms.ChoiceField(choices=CHOICES, required=True, widget=forms.RadioSelect, label="France vs Germany")
    game3 = forms.ChoiceField(choices=CHOICES, required=True, widget=forms.RadioSelect, label="Sweden vs Iceland")


def index(request):
    if request.method == "POST":
        form = GroupGamesForm(request.POST)
        if form.is_valid():
            for data in form.cleaned_data:
                submissions.append(data)
            return HttpResponseRedirect(reverse("enter:confirm"))
        else:
            return render(request, "enter/index.html", {
                "form": form
            })

    return render(request, "enter/index.html", {
        "games": games,
        "form": GroupGamesForm()
    })


def confirm(request):
    return render(request, "enter/confirm.html", {
        "submissions": submissions
    })


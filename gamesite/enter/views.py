from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

games = ["foo", "bar", "baz"]
CHOICES = [("home", "Home"), ("draw", "Draw"), ("away", "Away")]
submissions = []


class GroupGamesForm(forms.Form):
    game1 = forms.ChoiceField(choices=CHOICES, required=True, widget=forms.RadioSelect, label="Turkey vs Italy")
    game2 = forms.ChoiceField(choices=CHOICES, required=True, widget=forms.RadioSelect, label="Wales vs Switzerland")
    game3 = forms.ChoiceField(choices=CHOICES, required=True, widget=forms.RadioSelect, label="England vs Crotia")


def index(request, form_class=GroupGamesForm, template_name="enter/index.html", success_url="enter:confirm"):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            for data in form.cleaned_data:
                submissions.append(data)
            return HttpResponseRedirect(reverse(success_url))
        else:
            return render(request, template_name, {
                "form": form
            })

    return render(request, template_name, {
        "games": games,
        "form": form_class()
    })


def confirm(request):
    return render(request, "enter/confirm.html", {
        "submissions": submissions
    })


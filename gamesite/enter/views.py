from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import GroupMatchForm, GroupMatchOutcomeForm
from .models import GroupMatch, GroupMatchOutcome

games = ["foo", "bar", "baz"]
submissions = []


class GroupGamesForm1(forms.Form):
    CHOICES = [("home", "Home"), ("draw", "Draw"), ("away", "Away")]
    game1 = forms.ChoiceField(choices=CHOICES, required=True, widget=forms.RadioSelect, label="Turkey vs Italy")
    game2 = forms.ChoiceField(choices=CHOICES, required=True, widget=forms.RadioSelect, label="Wales vs Switzerland")
    game3 = forms.ChoiceField(choices=CHOICES, required=True, widget=forms.RadioSelect, label="England vs Crotia")


class GroupGamesForm2(forms.Form):
    match1 = forms.ModelChoiceField(queryset=GroupMatch.objects.first().groupmatchoutcome_set.all())


def index(request, form_class=GroupGamesForm1, template_name="enter/index.html", success_url="enter:confirm"):
    matches = GroupMatch.objects.all()
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            for data in form.cleaned_data:
                submissions.append(data)
            return HttpResponseRedirect(reverse(success_url))
        else:
            return render(request, template_name, {
                "title": "Enter",
                "form": form
            })

    return render(request, template_name, {
        "title": "Enter",
        "matches": matches,
        "form": form_class()
    })


def confirm(request):
    return render(request, "enter/confirm.html", {
        "title": "Review and Confirm",
        "submissions": submissions
    })


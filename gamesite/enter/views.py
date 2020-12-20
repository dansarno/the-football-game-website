from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import GroupMatchOutcomeForm

submissions = []


def index(request, form_class=GroupMatchOutcomeForm, template_name="enter/index.html", success_url="enter:confirm"):
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
        "form": form_class()
    })


def confirm(request):
    return render(request, "enter/confirm.html", {
        "title": "Review and Confirm",
        "submissions": submissions
    })


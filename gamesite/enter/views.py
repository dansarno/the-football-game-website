from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import GroupMatchOutcomeForm
from .models import GroupMatchBet


@login_required
def index(request, form_class=GroupMatchOutcomeForm, template_name="enter/index.html", success_url="enter:confirm"):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            for field_name, field_value in form.cleaned_data.items():
                bet = GroupMatchBet(bet=field_value, entry=request.user.profile.entry_set.first())
                bet.save()
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


@login_required
def confirm(request):
    return render(request, "enter/confirm.html", {
        "title": "Review and Confirm"
    })


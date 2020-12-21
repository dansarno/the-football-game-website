from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import GroupMatchOutcomeForm
from .models import GroupMatchBet, Entry


@login_required
def index(request, form_class=GroupMatchOutcomeForm, template_name="enter/index.html", success_url="enter:confirm"):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            if not request.user.profile.entry_set.all():
                new_entry = Entry(profile=request.user.profile)
                new_entry.save()
            for field_name, field_value in form.cleaned_data.items():
                existing_bet = GroupMatchBet.objects.filter(bet__match=field_value.match,
                                                            entry=request.user.profile.entry_set.first()
                                                            # TODO need to change first()
                                                            ).first()
                if existing_bet:
                    existing_bet.bet = field_value
                    existing_bet.save()
                else:
                    new_bet = GroupMatchBet(bet=field_value,
                                            entry=request.user.profile.entry_set.first())  # TODO need to change first()
                    new_bet.save()
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

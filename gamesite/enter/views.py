from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import GroupMatchOutcomeForm, TournamentBetGroupForm
from .models import GroupMatchBet, TournamentBetGroup, Entry


@login_required
def index(request, template_name="enter/index.html", success_url="enter:confirm"):
    if request.method == "POST":
        group_matches_form = GroupMatchOutcomeForm(request.POST)
        tournament_bets_form = TournamentBetGroupForm(request.POST)
        # Add other forms here
        print(tournament_bets_form.errors)
        if group_matches_form.is_valid() and tournament_bets_form.is_valid():
            existing_entries = request.user.profile.entry_set.all()
            if not existing_entries:
                new_entry = Entry(profile=request.user.profile)
                new_entry.save()
            for field_name, field_value in group_matches_form.cleaned_data.items():
                existing_match_bet = GroupMatchBet.objects.filter(bet__match=field_value.match,
                                                                  entry=request.user.profile.entry_set.first()
                                                                  # TODO need to change first()
                                                                  ).first()
                if existing_match_bet:
                    existing_match_bet.bet = field_value
                    existing_match_bet.save()
                else:
                    new_bet = GroupMatchBet(bet=field_value,
                                            entry=request.user.profile.entry_set.first())  # TODO need to change first()
                    new_bet.save()

            existing_tournament_bets = TournamentBetGroup.objects.filter(entry=request.user.profile.entry_set.first()
                                                                         # TODO need to change first()
                                                                         ).first()
            if existing_tournament_bets:
                existing_tournament_bets.delete()  # Seems insecure!!!
            tournament_bets = tournament_bets_form.save(commit=False)
            tournament_bets.entry = request.user.profile.entry_set.first()  # TODO need to change first()
            tournament_bets.save()
            return HttpResponseRedirect(reverse(success_url))
        else:
            return render(request, template_name, {
                "title": "Enter",
                "group_matches_form": group_matches_form,
                "tournament_bets_form": tournament_bets_form
            })

    return render(request, template_name, {
        "title": "Enter",
        "group_matches_form": GroupMatchOutcomeForm(),
        "tournament_bets_form": TournamentBetGroupForm()
        # instance=request.user.profile.entry_set.first().tournamentbetgroup
    })


@login_required
def confirm(request):
    return render(request, "enter/confirm.html", {
        "title": "Review and Confirm"
    })

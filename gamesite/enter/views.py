from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from . import forms
from . import models


@login_required
def index(request):
    existing_entries = request.user.profile.entry_set.all()
    return render(request, "enter/index.html", {
        "title": "Entry Manager",
        "entries": existing_entries
    })


@login_required
def entry(request, entry_id, template_name="enter/entry.html", success_url="enter:index"):
    requested_entry = get_object_or_404(models.Entry, id=entry_id)

    if request.user != requested_entry.profile.user:
        raise PermissionDenied

    if request.method == "POST":
        group_matches_form = forms.GroupMatchOutcomeForm(request.POST)
        tournament_bets_form = forms.TournamentBetGroupForm(request.POST)
        final_bets_form = forms.FinalBetGroupForm(request.POST)
        best_teams_success_bets_form = forms.BestTeamsSuccessBetGroupForm(request.POST)
        group_winner_bets_form = forms.GroupWinnerOutcomeForm(request.POST)
        fifty_fifty_bets_form = forms.FiftyFiftyOutcomeForm(request.POST)
        top_goal_group_bets_form = forms.TopGoalScoringGroupBetForm(request.POST)
        top_goal_player_bets_form = forms.TopGoalScoringPlayerBetForm(request.POST)
        if (group_matches_form.is_valid() and tournament_bets_form.is_valid() and final_bets_form.is_valid()
                and best_teams_success_bets_form.is_valid() and group_winner_bets_form.is_valid() and
                fifty_fifty_bets_form.is_valid()):
            existing_entries = request.user.profile.entry_set.all()
            if not existing_entries:
                new_entry = models.Entry(profile=request.user.profile)
                new_entry.save()
            for field_name, field_value in group_matches_form.cleaned_data.items():
                existing_match_bet = models.GroupMatchBet.objects.filter(bet__match=field_value.match,
                                                                         entry=requested_entry).first()
                if existing_match_bet:
                    existing_match_bet.bet = field_value
                    existing_match_bet.save()
                else:
                    new_bet = models.GroupMatchBet(bet=field_value, entry=requested_entry)
                    new_bet.save()

            for field_name, field_value in group_winner_bets_form.cleaned_data.items():
                existing_group_winner_bet = models.GroupWinnerBet.objects.filter(bet__group=field_value.group,
                                                                                 entry=requested_entry).first()
                if existing_group_winner_bet:
                    existing_group_winner_bet.bet = field_value
                    existing_group_winner_bet.save()
                else:
                    new_bet = models.GroupWinnerBet(bet=field_value, entry=requested_entry)
                    new_bet.save()

            for field_name, field_value in fifty_fifty_bets_form.cleaned_data.items():
                existing_fifty_fifty_bet = models.FiftyFiftyBet.objects.filter(bet__fifty_fifty=field_value.fifty_fifty,
                                                                               entry=requested_entry).first()
                if existing_fifty_fifty_bet:
                    existing_fifty_fifty_bet.bet = field_value
                    existing_fifty_fifty_bet.save()
                else:
                    new_bet = models.FiftyFiftyBet(bet=field_value, entry=requested_entry)
                    new_bet.save()

            existing_tournament_bets = models.TournamentBetGroup.objects.filter(entry=requested_entry).first()
            existing_final_bets = models.FinalBetGroup.objects.filter(entry=requested_entry).first()
            existing_top_teams_bets = models.BestTeamsSuccessBetGroup.objects.filter(entry=requested_entry).first()
            existing_top_goal_group_bet = models.TopGoalscoringGroupBet.objects.filter(entry=requested_entry).first()
            existing_top_goal_player_bet = models.TopGoalscoringPlayerBet.objects.filter(entry=requested_entry).first()
            if existing_tournament_bets:
                existing_tournament_bets.delete()  # Seems insecure!!!
            if existing_final_bets:
                existing_final_bets.delete()  # Seems insecure!!!
            if existing_top_teams_bets:
                existing_top_teams_bets.delete()  # Seems insecure!!!
            if existing_top_goal_group_bet:
                existing_top_goal_group_bet.delete()  # Seems insecure!!!
            if existing_top_goal_player_bet:
                existing_top_goal_player_bet.delete()  # Seems insecure!!!

            tournament_bets = tournament_bets_form.save(commit=False)
            tournament_bets.entry = requested_entry
            tournament_bets.save()
            final_bets = final_bets_form.save(commit=False)
            final_bets.entry = requested_entry
            final_bets.save()
            best_teams_success_bets = best_teams_success_bets_form.save(commit=False)
            best_teams_success_bets.entry = requested_entry
            best_teams_success_bets.save()
            top_goal_group_bet = top_goal_group_bets_form.save(commit=False)
            top_goal_group_bet.entry = requested_entry
            top_goal_group_bet.save()
            top_goal_player_bet = top_goal_player_bets_form.save(commit=False)
            top_goal_player_bet.entry = requested_entry
            top_goal_player_bet.save()
            return HttpResponseRedirect(reverse(success_url))
        else:
            return render(request, template_name, {
                "title": "Enter",
                "group_matches_form": group_matches_form,
                "tournament_bets_form": tournament_bets_form,
                "final_bets_form": final_bets_form,
                "best_teams_success_bets_form": best_teams_success_bets_form,
                "group_winner_bets_form": group_winner_bets_form,
                "fifty_fifty_bets_form": fifty_fifty_bets_form,
                "top_goal_group_bets_form": top_goal_group_bets_form,
                "top_goal_player_bets_form": top_goal_player_bets_form
            })

    return render(request, template_name, {
        "title": "Enter",
        "group_matches_form": forms.GroupMatchOutcomeForm(),
        "tournament_bets_form": forms.TournamentBetGroupForm(),
        # instance=request.user.profile.entry_set.first().tournamentbetgroup
        "final_bets_form": forms.FinalBetGroupForm(),
        "best_teams_success_bets_form": forms.BestTeamsSuccessBetGroupForm(),
        "group_winner_bets_form": forms.GroupWinnerOutcomeForm(),
        "fifty_fifty_bets_form": forms.FiftyFiftyOutcomeForm(),
        "top_goal_group_bets_form": forms.TopGoalScoringGroupBetForm(),
        "top_goal_player_bets_form": forms.TopGoalScoringPlayerBetForm()
    })


@login_required
def confirm(request):
    return render(request, "enter/confirm.html", {
        "title": "Review and Confirm"
    })

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
def create_entry(request, template_name="enter/entry.html", success_url="enter:index"):

    if request.method == "POST":
        group_matches_form = forms.GroupMatchOutcomeForm(request.POST)
        tournament_bets_form = forms.TournamentBetGroupForm(request.POST)
        final_bets_form = forms.FinalBetGroupForm(request.POST)
        best_teams_success_bets_form = forms.BestTeamsSuccessBetGroupForm(request.POST)
        group_winners_form = forms.GroupWinnerOutcomeForm(request.POST)
        fifty_fifty_bets_form = forms.FiftyFiftyOutcomeForm(request.POST)
        top_goal_group_bets_form = forms.TopGoalScoringGroupBetForm(request.POST)
        top_goal_player_bets_form = forms.TopGoalScoringPlayerBetForm(request.POST)

        if (group_matches_form.is_valid() and
                tournament_bets_form.is_valid() and
                final_bets_form.is_valid() and
                best_teams_success_bets_form.is_valid() and
                group_winners_form.is_valid() and
                fifty_fifty_bets_form.is_valid()):

            new_entry = models.Entry(profile=request.user.profile)
            new_entry.save()

            for field_name, field_value in group_winners_form.cleaned_data.items():
                models.GroupWinnerBet.objects.create(group_winner_choice=field_value, entry=new_entry)

            match_bets = group_matches_form.save(commit=False)
            match_bets.entry = new_entry
            match_bets.save()
            # group_winners_bets = group_winners_form.save(commit=False)
            # group_winners_bets.entry = new_entry
            # group_winners_bets.save()
            tournament_bets = tournament_bets_form.save(commit=False)
            tournament_bets.entry = new_entry
            tournament_bets.save()
            final_bets = final_bets_form.save(commit=False)
            final_bets.entry = new_entry
            final_bets.save()
            best_teams_success_bets = best_teams_success_bets_form.save(commit=False)
            best_teams_success_bets.entry = new_entry
            best_teams_success_bets.save()
            top_goal_group_bet = top_goal_group_bets_form.save(commit=False)
            top_goal_group_bet.entry = new_entry
            top_goal_group_bet.save()
            top_goal_player_bet = top_goal_player_bets_form.save(commit=False)
            top_goal_player_bet.entry = new_entry
            top_goal_player_bet.save()
            fifty_fifty_bets = fifty_fifty_bets_form.save(commit=False)
            fifty_fifty_bets.entry = new_entry
            fifty_fifty_bets.save()

            return HttpResponseRedirect(reverse(success_url))
    else:
        group_matches_form = forms.GroupMatchOutcomeForm()
        tournament_bets_form = forms.TournamentBetGroupForm()
        final_bets_form = forms.FinalBetGroupForm()
        best_teams_success_bets_form = forms.BestTeamsSuccessBetGroupForm()
        group_winners_form = forms.GroupWinnerOutcomeForm()
        fifty_fifty_bets_form = forms.FiftyFiftyOutcomeForm()
        top_goal_group_bets_form = forms.TopGoalScoringGroupBetForm()
        top_goal_player_bets_form = forms.TopGoalScoringPlayerBetForm()

    return render(request, template_name, {
        "title": "Enter",
        "group_matches_form": group_matches_form,
        "tournament_bets_form": tournament_bets_form,
        "final_bets_form": final_bets_form,
        "best_teams_success_bets_form": best_teams_success_bets_form,
        "group_winner_bets_form": group_winners_form,
        "fifty_fifty_bets_form": fifty_fifty_bets_form,
        "top_goal_group_bets_form": top_goal_group_bets_form,
        "top_goal_player_bets_form": top_goal_player_bets_form
    })


@login_required
def create_random_entry(request, template_name="enter/entry.html", success_url="enter:index"):
    pass


@login_required
def edit_entry(request, entry_id, template_name="enter/entry.html", success_url="enter:index"):
    requested_entry = get_object_or_404(models.Entry, id=entry_id)

    if request.user != requested_entry.profile.user:
        raise PermissionDenied

    if request.method == "POST":
        group_matches_form = forms.GroupMatchOutcomeForm(request.POST, instance=requested_entry.groupmatchbetgroup)
        tournament_bets_form = forms.TournamentBetGroupForm(request.POST, instance=requested_entry.tournamentbetgroup)
        final_bets_form = forms.FinalBetGroupForm(request.POST, instance=requested_entry.finalbetgroup)
        best_teams_success_bets_form = forms.BestTeamsSuccessBetGroupForm(request.POST, instance=requested_entry.bestteamssuccessbetgroup)
        group_winners_form = forms.GroupWinnerOutcomeForm(request.POST, instance=requested_entry.groupwinnerbetgroup)
        fifty_fifty_bets_form = forms.FiftyFiftyOutcomeForm(request.POST, instance=requested_entry.fiftyfiftybetgroup)
        top_goal_group_bets_form = forms.TopGoalScoringGroupBetForm(request.POST, instance=requested_entry.topgoalscoringgroupbet)
        top_goal_player_bets_form = forms.TopGoalScoringPlayerBetForm(request.POST, instance=requested_entry.topgoalscoringplayerbet)

        if (group_matches_form.is_valid() and
                tournament_bets_form.is_valid() and
                final_bets_form.is_valid() and
                best_teams_success_bets_form.is_valid() and
                group_winners_form.is_valid() and
                fifty_fifty_bets_form.is_valid()):

            match_bets = group_matches_form.save(commit=False)
            match_bets.entry = requested_entry
            match_bets.save()
            group_winners_bets = group_winners_form.save(commit=False)
            group_winners_bets.entry = requested_entry
            group_winners_bets.save()
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
            fifty_fifty_bets = fifty_fifty_bets_form.save(commit=False)
            fifty_fifty_bets.entry = requested_entry
            fifty_fifty_bets.save()

            requested_entry.save()

            return HttpResponseRedirect(reverse(success_url))
    else:
        group_matches_form = forms.GroupMatchOutcomeForm(instance=requested_entry.groupmatchbetgroup)
        tournament_bets_form = forms.TournamentBetGroupForm(instance=requested_entry.tournamentbetgroup)
        final_bets_form = forms.FinalBetGroupForm(instance=requested_entry.finalbetgroup)
        best_teams_success_bets_form = forms.BestTeamsSuccessBetGroupForm(instance=requested_entry.bestteamssuccessbetgroup)
        group_winner_bets = models.GroupWinnerBet.objects.filter(entry=requested_entry)
        data = {'group_a_winner_bet': group_winner_bets[0].group_winner_choice,
                'group_b_winner_bet': group_winner_bets[1].group_winner_choice,
                'group_c_winner_bet': group_winner_bets[2].group_winner_choice,
                'group_d_winner_bet': group_winner_bets[3].group_winner_choice,
                'group_e_winner_bet': group_winner_bets[4].group_winner_choice,
                'group_f_winner_bet': group_winner_bets[5].group_winner_choice
                }
        group_winners_form = forms.GroupWinnerOutcomeForm(initial=data)
        fifty_fifty_bets_form = forms.FiftyFiftyOutcomeForm(instance=requested_entry.fiftyfiftybetgroup)
        tsg_bet = models.TopGoalscoringGroupBet.objects.get(entry=requested_entry)
        data = {'group_choice': tsg_bet.group_choice}
        top_goal_group_bets_form = forms.TopGoalScoringGroupBetForm(initial=data)
        tsp_bet = models.TopGoalscoringPlayerBet.objects.get(entry=requested_entry)
        data = {'choice': tsp_bet.choice}
        top_goal_player_bets_form = forms.TopGoalScoringPlayerBetForm(initial=data)

    return render(request, template_name, {
        "title": "Enter",
        "group_matches_form": group_matches_form,
        "tournament_bets_form": tournament_bets_form,
        "final_bets_form": final_bets_form,
        "best_teams_success_bets_form": best_teams_success_bets_form,
        "group_winner_bets_form": group_winners_form,
        "fifty_fifty_bets_form": fifty_fifty_bets_form,
        "top_goal_group_bets_form": top_goal_group_bets_form,
        "top_goal_player_bets_form": top_goal_player_bets_form
    })


@login_required
def delete_entry(request, entry_id, success_url="enter:index"):
    requested_entry = get_object_or_404(models.Entry, id=entry_id)

    if request.user != requested_entry.profile.user:
        raise PermissionDenied

    requested_entry.delete()

    return HttpResponseRedirect(reverse(success_url))


@login_required
def confirm(request):
    return render(request, "enter/confirm.html", {
        "title": "Review and Confirm"
    })

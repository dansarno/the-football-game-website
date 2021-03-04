from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from . import forms
from . import models
from random import choice


@login_required
def index(request):
    existing_entries = request.user.profile.entries.order_by('id')
    return render(request, "enter/index.html", {
        "title": "Entry Manager",
        "entries": existing_entries
    })


@login_required
def leaderboard(request):
    return render(request, "enter/leader_board.html", {
        "title": "Leader Board"
    })


@login_required
def results(request):
    game_progress_percentage = int((models.CalledBet.objects.count() / models.ChoiceGroup.objects.count()) * 100)

    game_section_progress = []
    for category in models.GameCategory.objects.all().order_by('order'):
        game_section = dict()
        numerator = models.CalledBet.objects.filter(outcome__choice_group__game_category=category).count()
        denominator = models.ChoiceGroup.objects.filter(game_category=category).count()
        if denominator == 0:
            complete = 0
        else:
            complete = (numerator / denominator) * 100
        game_section['title'] = category.title
        game_section['percentage'] = complete
        game_section['number_completed'] = numerator
        game_section['total_number'] = denominator
        game_section_progress.append(game_section)

    return render(request, "enter/results.html", {
        "title": "Results",
        'game_progress': game_progress_percentage,
        'section_progress': game_section_progress
    })


@login_required
def create_entry(request, template_name="enter/entry.html", success_url="enter:index"):
    # if request.method == "POST":
        # group_matches_form = forms.GroupMatchOutcomeForm(request.POST)
        # tournament_bets_form = forms.TournamentBetGroupForm(request.POST)
        # final_bets_form = forms.FinalBetGroupForm(request.POST)
        # best_teams_success_bets_form = forms.BestTeamsSuccessBetGroupForm(request.POST)
        # group_winners_form = forms.GroupWinnerOutcomeForm(request.POST)
        # fifty_fifty_bets_form = forms.FiftyFiftyOutcomeForm(request.POST)
        # top_goal_group_bets_form = forms.TopGoalScoringGroupBetForm(request.POST)
        # top_goal_player_bets_form = forms.TopGoalScoringPlayerBetForm(request.POST)

        # if (top_goal_group_bets_form.is_valid() and
        #         top_goal_player_bets_form.is_valid() and
        #         fifty_fifty_bets_form.is_valid() and
        #         best_teams_success_bets_form.is_valid()):
        #     new_entry = models.Entry.objects.create(profile=request.user.profile)

            # for field_name, field_value in group_winners_form.cleaned_data.items():
            #     models.GroupWinnerBet.objects.create(group_winner_choice=field_value, entry=new_entry)

            # match_bets = group_matches_form.save(commit=False)
            # match_bets.entry = new_entry
            # match_bets.save()
            # # group_winners_bets = group_winners_form.save(commit=False)
            # # group_winners_bets.entry = new_entry
            # # group_winners_bets.save()
            # tournament_bets = tournament_bets_form.save(commit=False)
            # tournament_bets.entry = new_entry
            # tournament_bets.save()
            # final_bets = final_bets_form.save(commit=False)
            # final_bets.entry = new_entry
            # final_bets.save()
            # best_teams_success_bets = best_teams_success_bets_form.save(commit=False)
            # best_teams_success_bets.entry = new_entry
            # best_teams_success_bets.save()

            # group_choice = top_goal_group_bets_form.cleaned_data['group_choice']
            # models.Bet.objects.create(outcome=group_choice, entry=new_entry)
            #
            # choice = top_goal_player_bets_form.cleaned_data['choice']
            # models.Bet.objects.create(outcome=choice, entry=new_entry)
            #
            # for field_name, field_value in fifty_fifty_bets_form.cleaned_data.items():
            #     models.Bet.objects.create(outcome=field_value, entry=new_entry)
            #
            # for field_name, field_value in best_teams_success_bets_form.cleaned_data.items():
            #     models.Bet.objects.create(outcome=field_value, entry=new_entry)
    #
    #         return HttpResponseRedirect(reverse(success_url))
    # else:
    #     # group_matches_form = forms.GroupMatchOutcomeForm()
    #     # tournament_bets_form = forms.TournamentBetGroupForm()
    #     # final_bets_form = forms.FinalBetGroupForm()
    #     best_teams_success_bets_form = forms.BestTeamsSuccessBetGroupForm()
    #     # group_winners_form = forms.GroupWinnerOutcomeForm()
    #     fifty_fifty_bets_form = forms.FiftyFiftyOutcomeForm()
    #     top_goal_group_bets_form = forms.TopGoalScoringGroupBetForm()
    #     top_goal_player_bets_form = forms.TopGoalScoringPlayerBetForm()

    return render(request, template_name, {
        "title": "Enter",
        # "group_matches_form": group_matches_form,
        # "tournament_bets_form": tournament_bets_form,
        # "final_bets_form": final_bets_form,
        # "best_teams_success_bets_form": best_teams_success_bets_form,
        # "group_winner_bets_form": group_winners_form,
        # "fifty_fifty_bets_form": fifty_fifty_bets_form,
        # "top_goal_group_bets_form": top_goal_group_bets_form,
        # "top_goal_player_bets_form": top_goal_player_bets_form
    })


@login_required
def create_random_entry(request, success_url="enter:index"):
    new_entry = models.Entry.objects.create(profile=request.user.profile)
    for choice_group in models.ChoiceGroup.objects.all():
        random_choice = choice(choice_group.outcome_set.non_polymorphic().all())
        models.Bet.objects.create(entry=new_entry, outcome=random_choice)
    messages.add_message(request, messages.SUCCESS, 'Random entry created.')
    return HttpResponseRedirect(reverse(success_url))


@login_required
def edit_entry(request, entry_id, template_name="enter/entry.html", success_url="enter:index"):
    requested_entry = get_object_or_404(models.Entry, id=entry_id)

    if request.user != requested_entry.profile.user:
        raise PermissionDenied

    if request.method == "POST":
        # group_matches_form = forms.GroupMatchOutcomeForm(request.POST, instance=requested_entry.groupmatchbetgroup)
        # tournament_bets_form = forms.TournamentBetGroupForm(request.POST, instance=requested_entry.tournamentbetgroup)
        # final_bets_form = forms.FinalBetGroupForm(request.POST, instance=requested_entry.finalbetgroup)
        # best_teams_success_bets_form = forms.BestTeamsSuccessBetGroupForm(request.POST,
        #                                                                   instance=requested_entry.bestteamssuccessbetgroup)
        # group_winners_form = forms.GroupWinnerOutcomeForm(request.POST, instance=requested_entry.groupwinnerbetgroup)
        # fifty_fifty_bets_form = forms.FiftyFiftyOutcomeForm(request.POST, instance=requested_entry.fiftyfiftybetgroup)
        # top_goal_group_bets_form = forms.TopGoalScoringGroupBetForm(request.POST,
        #                                                             instance=requested_entry.topgoalscoringgroupbet)
        # top_goal_player_bets_form = forms.TopGoalScoringPlayerBetForm(request.POST,
        #                                                               instance=requested_entry.topgoalscoringplayerbet)

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
        best_teams_success_bets_form = forms.BestTeamsSuccessBetGroupForm(
            instance=requested_entry.bestteamssuccessbetgroup)
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
    num_of_user_entries = len(request.user.profile.entries.order_by('id'))

    if request.user != requested_entry.profile.user:
        raise PermissionDenied

    deleted_entry_label = requested_entry.label
    requested_entry.delete()

    if deleted_entry_label:
        msg = f"You have deleted Entry {deleted_entry_label}. "
    else:
        msg = f"You have deleted your entry"
    if deleted_entry_label == "A" and num_of_user_entries == 3:
        msg += "Entry B has now been labeled Entry A and Entry C has now been labeled Entry B."
    elif deleted_entry_label == "B" and num_of_user_entries == 3:
        msg += "Entry C has now been labeled Entry B."
    messages.add_message(request, messages.SUCCESS, msg)

    return HttpResponseRedirect(reverse(success_url))


@login_required
def submit_entry(request, entry_id, success_url="enter:index"):
    requested_entry = get_object_or_404(models.Entry, id=entry_id)

    if request.user != requested_entry.profile.user:
        raise PermissionDenied

    submitted_entry_label = requested_entry.label
    requested_entry.has_submitted = True
    requested_entry.save()

    if submitted_entry_label:
        msg = f"You have successfully submitted Entry {submitted_entry_label}. Good luck ☘"
    else:
        msg = f"You have successfully submitted your entry. Good luck ☘"
    messages.add_message(request, messages.SUCCESS, msg)

    return HttpResponseRedirect(reverse(success_url))


@login_required
def confirm(request):
    return render(request, "enter/confirm.html", {
        "title": "Review and Confirm"
    })

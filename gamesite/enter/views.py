from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import GroupMatchOutcomeForm, TournamentBetGroupForm, FinalBetGroupForm, BestTeamsSuccessBetGroupForm, \
    GroupWinnerOutcomeForm, FiftyFiftyOutcomeForm, TopGoalScoringGroupBetForm, TopGoalScoringPlayerBetForm
from .models import GroupMatchBet, TournamentBetGroup, FinalBetGroup, BestTeamsSuccessBetGroup, GroupWinnerBet, \
    FiftyFiftyBet, TopGoalscoringGroupBet, TopGoalscoringPlayerBet, Entry


@login_required
def index(request, template_name="enter/index.html", success_url="enter:confirm"):
    if request.method == "POST":
        group_matches_form = GroupMatchOutcomeForm(request.POST)
        tournament_bets_form = TournamentBetGroupForm(request.POST)
        final_bets_form = FinalBetGroupForm(request.POST)
        best_teams_success_bets_form = BestTeamsSuccessBetGroupForm(request.POST)
        group_winner_bets_form = GroupWinnerOutcomeForm(request.POST)
        fifty_fifty_bets_form = FiftyFiftyOutcomeForm(request.POST)
        top_goal_group_bets_form = TopGoalScoringGroupBetForm(request.POST)
        top_goal_player_bets_form = TopGoalScoringPlayerBetForm(request.POST)
        # Add other forms here
        if (group_matches_form.is_valid() and tournament_bets_form.is_valid() and final_bets_form.is_valid()
                and best_teams_success_bets_form.is_valid() and group_winner_bets_form.is_valid() and
                fifty_fifty_bets_form.is_valid()):
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

            for field_name, field_value in group_winner_bets_form.cleaned_data.items():
                existing_group_winner_bet = GroupWinnerBet.objects.filter(bet__group=field_value.group,
                                                                          entry=request.user.profile.entry_set.first()
                                                                          # TODO need to change first()
                                                                          ).first()
                if existing_group_winner_bet:
                    existing_group_winner_bet.bet = field_value
                    existing_group_winner_bet.save()
                else:
                    new_bet = GroupWinnerBet(bet=field_value,
                                             entry=request.user.profile.entry_set.first())  # TODO need to change first()
                    new_bet.save()

            for field_name, field_value in fifty_fifty_bets_form.cleaned_data.items():
                existing_fifty_fifty_bet = FiftyFiftyBet.objects.filter(bet__fifty_fifty=field_value.fifty_fifty,
                                                                        entry=request.user.profile.entry_set.first()
                                                                        # TODO need to change first()
                                                                        ).first()
                if existing_fifty_fifty_bet:
                    existing_fifty_fifty_bet.bet = field_value
                    existing_fifty_fifty_bet.save()
                else:
                    new_bet = FiftyFiftyBet(bet=field_value,
                                            entry=request.user.profile.entry_set.first())  # TODO need to change first()
                    new_bet.save()

            existing_tournament_bets = TournamentBetGroup.objects.filter(entry=request.user.profile.entry_set.first()
                                                                         # TODO need to change first()
                                                                         ).first()
            existing_final_bets = FinalBetGroup.objects.filter(entry=request.user.profile.entry_set.first()
                                                               # TODO need to change first()
                                                               ).first()
            existing_top_teams_bets = BestTeamsSuccessBetGroup.objects.filter(
                entry=request.user.profile.entry_set.first()
                # TODO need to change first()
            ).first()
            existing_top_goal_group_bet = TopGoalscoringGroupBet.objects.filter(
                entry=request.user.profile.entry_set.first()
                # TODO need to change first()
                ).first()
            existing_top_goal_player_bet = TopGoalscoringPlayerBet.objects.filter(
                entry=request.user.profile.entry_set.first()
                # TODO need to change first()
            ).first()
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
            tournament_bets.entry = request.user.profile.entry_set.first()  # TODO need to change first()
            tournament_bets.save()
            final_bets = final_bets_form.save(commit=False)
            final_bets.entry = request.user.profile.entry_set.first()  # TODO need to change first()
            final_bets.save()
            best_teams_success_bets = best_teams_success_bets_form.save(commit=False)
            best_teams_success_bets.entry = request.user.profile.entry_set.first()  # TODO need to change first()
            best_teams_success_bets.save()
            top_goal_group_bet = top_goal_group_bets_form.save(commit=False)
            top_goal_group_bet.entry = request.user.profile.entry_set.first()  # TODO need to change first()
            top_goal_group_bet.save()
            top_goal_player_bet = top_goal_player_bets_form.save(commit=False)
            top_goal_player_bet.entry = request.user.profile.entry_set.first()  # TODO need to change first()
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
        "group_matches_form": GroupMatchOutcomeForm(),
        "tournament_bets_form": TournamentBetGroupForm(),
        # instance=request.user.profile.entry_set.first().tournamentbetgroup
        "final_bets_form": FinalBetGroupForm(),
        "best_teams_success_bets_form": BestTeamsSuccessBetGroupForm(),
        "group_winner_bets_form": GroupWinnerOutcomeForm(),
        "fifty_fifty_bets_form": FiftyFiftyOutcomeForm(),
        "top_goal_group_bets_form": TopGoalScoringGroupBetForm(),
        "top_goal_player_bets_form": TopGoalScoringPlayerBetForm()
    })


@login_required
def confirm(request):
    return render(request, "enter/confirm.html", {
        "title": "Review and Confirm"
    })

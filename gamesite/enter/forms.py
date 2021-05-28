from django import forms
from . import models

group_matches = models.GroupMatch.objects.order_by('ko_time', 'match_number')
fifty_fifty_questions = models.FiftyFiftyQuestion.objects.order_by('order')


class NameModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.winning_amount}'


class GroupMatchOutcomeForm(forms.Form):
    match1_bet = NameModelChoiceField(queryset=group_matches[0].groupmatchoutcome_set.all().order_by('-choice'),
                                      required=False,
                                      widget=forms.RadioSelect,
                                      label=group_matches[0])
    match2_bet = NameModelChoiceField(queryset=group_matches[1].groupmatchoutcome_set.all().order_by('-choice'),
                                      required=False,
                                      widget=forms.RadioSelect,
                                      label=group_matches[1])
    match3_bet = NameModelChoiceField(queryset=group_matches[2].groupmatchoutcome_set.all().order_by('-choice'),
                                      required=False,
                                      widget=forms.RadioSelect,
                                      label=group_matches[2])
    match4_bet = NameModelChoiceField(queryset=group_matches[3].groupmatchoutcome_set.all().order_by('-choice'),
                                      required=False,
                                      widget=forms.RadioSelect,
                                      label=group_matches[3])
    match5_bet = NameModelChoiceField(queryset=group_matches[4].groupmatchoutcome_set.all().order_by('-choice'),
                                      required=False,
                                      widget=forms.RadioSelect,
                                      label=group_matches[4])
    match6_bet = NameModelChoiceField(queryset=group_matches[5].groupmatchoutcome_set.all().order_by('-choice'),
                                      required=False,
                                      widget=forms.RadioSelect,
                                      label=group_matches[5])
    match7_bet = NameModelChoiceField(queryset=group_matches[6].groupmatchoutcome_set.all().order_by('-choice'),
                                      required=False,
                                      widget=forms.RadioSelect,
                                      label=group_matches[6])
    match8_bet = NameModelChoiceField(queryset=group_matches[7].groupmatchoutcome_set.all().order_by('-choice'),
                                      required=False,
                                      widget=forms.RadioSelect,
                                      label=group_matches[7])
    match9_bet = NameModelChoiceField(queryset=group_matches[8].groupmatchoutcome_set.all().order_by('-choice'),
                                      required=False,
                                      widget=forms.RadioSelect,
                                      label=group_matches[8])
    match10_bet = NameModelChoiceField(queryset=group_matches[9].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[9])
    match11_bet = NameModelChoiceField(queryset=group_matches[10].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[10])
    match12_bet = NameModelChoiceField(queryset=group_matches[11].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[11])
    match13_bet = NameModelChoiceField(queryset=group_matches[12].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[12])
    match14_bet = NameModelChoiceField(queryset=group_matches[13].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[13])
    match15_bet = NameModelChoiceField(queryset=group_matches[14].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[14])
    match16_bet = NameModelChoiceField(queryset=group_matches[15].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[15])
    match17_bet = NameModelChoiceField(queryset=group_matches[16].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[16])
    match18_bet = NameModelChoiceField(queryset=group_matches[17].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[17])
    match19_bet = NameModelChoiceField(queryset=group_matches[18].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[18])
    match20_bet = NameModelChoiceField(queryset=group_matches[19].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[19])
    match21_bet = NameModelChoiceField(queryset=group_matches[20].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[20])
    match22_bet = NameModelChoiceField(queryset=group_matches[21].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[21])
    match23_bet = NameModelChoiceField(queryset=group_matches[22].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[22])
    match24_bet = NameModelChoiceField(queryset=group_matches[23].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[23])
    match25_bet = NameModelChoiceField(queryset=group_matches[24].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[24])
    match26_bet = NameModelChoiceField(queryset=group_matches[25].groupmatchoutcome_set.all().order_by('-choice'),
                                       required=False,
                                       widget=forms.RadioSelect,
                                       label=group_matches[25])


class GroupWinnerOutcomeForm(forms.Form):
    group_a_winner_bet = NameModelChoiceField(queryset=models.GroupWinnerOutcome.objects.filter(group__name='A'),
                                              required=False,
                                              widget=forms.RadioSelect,
                                              label="Group A")
    group_b_winner_bet = NameModelChoiceField(queryset=models.GroupWinnerOutcome.objects.filter(group__name='B'),
                                              required=False,
                                              widget=forms.RadioSelect,
                                              label="Group B")
    group_c_winner_bet = NameModelChoiceField(queryset=models.GroupWinnerOutcome.objects.filter(group__name='C'),
                                              required=False,
                                              widget=forms.RadioSelect,
                                              label="Group C")
    group_d_winner_bet = NameModelChoiceField(queryset=models.GroupWinnerOutcome.objects.filter(group__name='D'),
                                              required=False,
                                              widget=forms.RadioSelect,
                                              label="Group D")
    group_e_winner_bet = NameModelChoiceField(queryset=models.GroupWinnerOutcome.objects.filter(group__name='E'),
                                              required=False,
                                              widget=forms.RadioSelect,
                                              label="Group E")
    group_f_winner_bet = NameModelChoiceField(queryset=models.GroupWinnerOutcome.objects.filter(group__name='F'),
                                              required=False,
                                              widget=forms.RadioSelect,
                                              label="Group F")


class TournamentTotalsForm(forms.Form):
    total_goals_bet = NameModelChoiceField(queryset=models.TournamentGoalsOutcome.objects.all().order_by('max_value'),
                                           required=False,
                                           widget=forms.RadioSelect,
                                           label="Total goals (ex. pen shootouts)")
    total_goals_in_a_game_bet = NameModelChoiceField(
        queryset=models.TournamentGoalsInAGameOutcome.objects.all().order_by('max_value'),
        required=False,
        widget=forms.RadioSelect,
        label="Most goals in a single game")
    total_own_goals_bet = NameModelChoiceField(
        queryset=models.TournamentOwnGoalsOutcome.objects.all().order_by('max_value'),
        required=False,
        widget=forms.RadioSelect,
        label="Total own goals")
    total_penalties_bet = NameModelChoiceField(
        queryset=models.TournamentPenaltiesOutcome.objects.all().order_by('max_value'),
        required=False,
        widget=forms.RadioSelect,
        label="Total penalties")


class DuringTheFinalForm(forms.Form):
    final_first_goal_bet = NameModelChoiceField(queryset=models.FinalFirstGoalOutcome.objects.all(),
                                                required=False,
                                                widget=forms.RadioSelect,
                                                label="First goal to be scored in the final")
    final_goals_bet = NameModelChoiceField(queryset=models.FinalGoalsOutcome.objects.all(),
                                           required=False,
                                           widget=forms.RadioSelect,
                                           label="Total goals (ex. pen shootout)")
    final_yellow_cards_bet = NameModelChoiceField(queryset=models.FinalYellowCardsOutcome.objects.all(),
                                                  required=False,
                                                  widget=forms.RadioSelect,
                                                  label="Number of yellow cards")
    final_ref_country_bet = NameModelChoiceField(queryset=models.FinalRefCountryOutcome.objects.all(),
                                                   required=False,
                                                   widget=forms.RadioSelect,
                                                   label="Nationality of the ref in the final")


class BestTeamsSuccessBetGroupForm(forms.Form):
    to_reach_semi_final_bet = NameModelChoiceField(
        queryset=models.ToReachSemiFinalOutcome.objects.all().order_by('team'),
        required=False,
        widget=forms.RadioSelect,
        label="To reach semi final")
    to_reach_final_bet = NameModelChoiceField(queryset=models.ToReachFinalOutcome.objects.all().order_by('team'),
                                              required=False,
                                              widget=forms.RadioSelect,
                                              label="To reach final")
    to_win_bet = NameModelChoiceField(queryset=models.ToWinOutcome.objects.all().order_by('team'),
                                      required=False,
                                      widget=forms.RadioSelect,
                                      label="To win Euros")
    highest_scoring_team_bet = NameModelChoiceField(
        queryset=models.HighestScoringTeamOutcome.objects.all().order_by('team'),
        required=False,
        widget=forms.RadioSelect,
        label="Highest scoring team")
    most_yellow_cards_bet = NameModelChoiceField(queryset=models.MostYellowCardsOutcome.objects.all().order_by('team'),
                                                 required=False,
                                                 widget=forms.RadioSelect,
                                                 label="Most yellows")
    fastest_yellow_card_bet = NameModelChoiceField(
        queryset=models.FastestYellowCardsOutcome.objects.all().order_by('team'),
        required=False,
        widget=forms.RadioSelect,
        label="Fastest yellow")
    fastest_tournament_goal_bet = NameModelChoiceField(
        queryset=models.FastestGoalOutcome.objects.all().order_by('team'),
        required=False,
        widget=forms.RadioSelect,
        label="Fastest Euro goal")
    most_clean_sheets_bet = NameModelChoiceField(
        queryset=models.MostCleanSheetsOutcome.objects.all().order_by('team'),
        required=False,
        widget=forms.RadioSelect,
        label="Most clean sheets")


class FiftyFiftyOutcomeForm(forms.Form):
    question1_bet = NameModelChoiceField(queryset=fifty_fifty_questions[0].fiftyfiftyoutcome_set.order_by('-choice'),
                                         required=False,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[0])
    question2_bet = NameModelChoiceField(queryset=fifty_fifty_questions[1].fiftyfiftyoutcome_set.order_by('-choice'),
                                         required=False,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[1])
    question3_bet = NameModelChoiceField(queryset=fifty_fifty_questions[2].fiftyfiftyoutcome_set.order_by('-choice'),
                                         required=False,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[2])
    question4_bet = NameModelChoiceField(queryset=fifty_fifty_questions[3].fiftyfiftyoutcome_set.order_by('-choice'),
                                         required=False,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[3])
    question5_bet = NameModelChoiceField(queryset=fifty_fifty_questions[4].fiftyfiftyoutcome_set.order_by('-choice'),
                                         required=False,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[4])
    question6_bet = NameModelChoiceField(queryset=fifty_fifty_questions[5].fiftyfiftyoutcome_set.order_by('-choice'),
                                         required=False,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[5])
    question7_bet = NameModelChoiceField(queryset=fifty_fifty_questions[6].fiftyfiftyoutcome_set.order_by('-choice'),
                                         required=False,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[6])
    question8_bet = NameModelChoiceField(queryset=fifty_fifty_questions[7].fiftyfiftyoutcome_set.order_by('-choice'),
                                         required=False,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[7])


class TopGoalScoringGroupBetForm(forms.Form):
    group_choice = NameModelChoiceField(queryset=models.TopGoalScoringGroupOutcome.objects.all().order_by('group__name'),
                                        required=False,
                                        widget=forms.RadioSelect)


class TopGoalScoringPlayerBetForm(forms.Form):
    choice = NameModelChoiceField(
        queryset=models.TopGoalScoringPlayerOutcome.objects.all().order_by('player__order'),
        required=False,
        widget=forms.RadioSelect)

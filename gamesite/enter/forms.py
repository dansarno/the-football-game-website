from django import forms
from .models import GroupMatch, TournamentBetGroup, TournamentGoalsOutcome, \
    TournamentOwnGoalsOutcome, TournamentHattricksOutcome, TournamentRedCardsOutcome, FinalBetGroup, \
    FinalFirstGoalOutcome, FinalRefContinentOutcome, FinalGoalsOutcome, FinalYellowCardsOutcome, FinalOwnGoalOutcome, \
    BestTeamsSuccessBetGroup, ToReachSemiFinalOutcome, ToReachFinalOutcome, ToWinOutcome, HighestScoringTeamOutcome, \
    MostYellowCardsOutcome, FastestYellowCardsOutcome, FastestGoalOutcome, GroupWinnerOutcome, FiftyFiftyQuestion

group_matches = GroupMatch.objects.all().order_by('ko_time')
fifty_fifty_questions = FiftyFiftyQuestion.objects.all()


class NameModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.winning_amount}'


class GroupMatchOutcomeForm(forms.Form):
    match1 = NameModelChoiceField(queryset=group_matches[0].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=group_matches[0])
    match2 = NameModelChoiceField(queryset=group_matches[1].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=group_matches[1])
    match3 = NameModelChoiceField(queryset=group_matches[2].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=group_matches[2])
    match4 = NameModelChoiceField(queryset=group_matches[3].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=group_matches[3])
    match5 = NameModelChoiceField(queryset=group_matches[4].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=group_matches[4])
    match6 = NameModelChoiceField(queryset=group_matches[5].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=group_matches[5])
    match7 = NameModelChoiceField(queryset=group_matches[6].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=group_matches[6])
    match8 = NameModelChoiceField(queryset=group_matches[7].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=group_matches[7])
    match9 = NameModelChoiceField(queryset=group_matches[8].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=group_matches[8])
    match10 = NameModelChoiceField(queryset=group_matches[9].groupmatchoutcome_set.all().order_by('-outcome'),
                                   required=True,
                                   widget=forms.RadioSelect,
                                   label=group_matches[9])
    match11 = NameModelChoiceField(queryset=group_matches[10].groupmatchoutcome_set.all().order_by('-outcome'),
                                   required=True,
                                   widget=forms.RadioSelect,
                                   label=group_matches[10])
    match12 = NameModelChoiceField(queryset=group_matches[11].groupmatchoutcome_set.all().order_by('-outcome'),
                                   required=True,
                                   widget=forms.RadioSelect,
                                   label=group_matches[11])
    match13 = NameModelChoiceField(queryset=group_matches[12].groupmatchoutcome_set.all().order_by('-outcome'),
                                   required=True,
                                   widget=forms.RadioSelect,
                                   label=group_matches[12])
    match14 = NameModelChoiceField(queryset=group_matches[13].groupmatchoutcome_set.all().order_by('-outcome'),
                                   required=True,
                                   widget=forms.RadioSelect,
                                   label=group_matches[13])
    match15 = NameModelChoiceField(queryset=group_matches[14].groupmatchoutcome_set.all().order_by('-outcome'),
                                   required=True,
                                   widget=forms.RadioSelect,
                                   label=group_matches[14])
    match16 = NameModelChoiceField(queryset=group_matches[15].groupmatchoutcome_set.all().order_by('-outcome'),
                                   required=True,
                                   widget=forms.RadioSelect,
                                   label=group_matches[15])
    match17 = NameModelChoiceField(queryset=group_matches[16].groupmatchoutcome_set.all().order_by('-outcome'),
                                   required=True,
                                   widget=forms.RadioSelect,
                                   label=group_matches[16])
    match18 = NameModelChoiceField(queryset=group_matches[17].groupmatchoutcome_set.all().order_by('-outcome'),
                                   required=True,
                                   widget=forms.RadioSelect,
                                   label=group_matches[17])
    match19 = NameModelChoiceField(queryset=group_matches[18].groupmatchoutcome_set.all().order_by('-outcome'),
                                   required=True,
                                   widget=forms.RadioSelect,
                                   label=group_matches[18])
    match20 = NameModelChoiceField(queryset=group_matches[19].groupmatchoutcome_set.all().order_by('-outcome'),
                                   required=True,
                                   widget=forms.RadioSelect,
                                   label=group_matches[19])
    match21 = NameModelChoiceField(queryset=group_matches[20].groupmatchoutcome_set.all().order_by('-outcome'),
                                   required=True,
                                   widget=forms.RadioSelect,
                                   label=group_matches[20])
    match22 = NameModelChoiceField(queryset=group_matches[21].groupmatchoutcome_set.all().order_by('-outcome'),
                                   required=True,
                                   widget=forms.RadioSelect,
                                   label=group_matches[21])


class GroupWinnerOutcomeForm(forms.Form):
    group_a_winner_bet = NameModelChoiceField(queryset=GroupWinnerOutcome.objects.filter(group__name='A'),
                                              required=True,
                                              widget=forms.RadioSelect,
                                              label="Group A")
    group_b_winner_bet = NameModelChoiceField(queryset=GroupWinnerOutcome.objects.filter(group__name='B'),
                                              required=True,
                                              widget=forms.RadioSelect,
                                              label="Group B")
    group_c_winner_bet = NameModelChoiceField(queryset=GroupWinnerOutcome.objects.filter(group__name='C'),
                                              required=True,
                                              widget=forms.RadioSelect,
                                              label="Group C")
    group_d_winner_bet = NameModelChoiceField(queryset=GroupWinnerOutcome.objects.filter(group__name='D'),
                                              required=True,
                                              widget=forms.RadioSelect,
                                              label="Group D")
    group_e_winner_bet = NameModelChoiceField(queryset=GroupWinnerOutcome.objects.filter(group__name='E'),
                                              required=True,
                                              widget=forms.RadioSelect,
                                              label="Group E")
    group_f_winner_bet = NameModelChoiceField(queryset=GroupWinnerOutcome.objects.filter(group__name='F'),
                                              required=True,
                                              widget=forms.RadioSelect,
                                              label="Group F")


class TournamentBetGroupForm(forms.ModelForm):
    total_goals_bet = NameModelChoiceField(queryset=TournamentGoalsOutcome.objects.all().order_by('min_value'),
                                           required=True,
                                           widget=forms.RadioSelect,
                                           label="Total tournament goals (excluding penalty shootouts)")
    total_red_cards_bet = NameModelChoiceField(queryset=TournamentRedCardsOutcome.objects.all().order_by('min_value'),
                                               required=True,
                                               widget=forms.RadioSelect,
                                               label="Total tournament red cards")
    total_own_goals_bet = NameModelChoiceField(queryset=TournamentOwnGoalsOutcome.objects.all().order_by('min_value'),
                                               required=True,
                                               widget=forms.RadioSelect,
                                               label="Total tournament own goals")
    total_hattricks_bet = NameModelChoiceField(queryset=TournamentHattricksOutcome.objects.all().order_by('min_value'),
                                               required=True,
                                               widget=forms.RadioSelect,
                                               label="Total hattricks")

    class Meta:
        model = TournamentBetGroup
        exclude = ('entry',)


class FinalBetGroupForm(forms.ModelForm):
    final_first_goal_bet = NameModelChoiceField(queryset=FinalFirstGoalOutcome.objects.all(),
                                                required=True,
                                                widget=forms.RadioSelect,
                                                label="First goal to be scored in the final")
    final_own_goals_bet = NameModelChoiceField(queryset=FinalOwnGoalOutcome.objects.all(),
                                               required=True,
                                               widget=forms.RadioSelect,
                                               label="There will be an own goal")
    final_yellow_cards_bet = NameModelChoiceField(queryset=FinalYellowCardsOutcome.objects.all(),
                                                  required=True,
                                                  widget=forms.RadioSelect,
                                                  label="Number of yellow cards")
    final_ref_continent_bet = NameModelChoiceField(queryset=FinalRefContinentOutcome.objects.all(),
                                                   required=True,
                                                   widget=forms.RadioSelect,
                                                   label="Continent of the ref in the final")
    final_goals_bet = NameModelChoiceField(queryset=FinalGoalsOutcome.objects.all(),
                                           required=True,
                                           widget=forms.RadioSelect,
                                           label="Total goals in the final (excluding a penalty shootout)")

    class Meta:
        model = FinalBetGroup
        exclude = ('entry',)


class BestTeamsSuccessBetGroupForm(forms.ModelForm):
    to_reach_semi_final_bet = NameModelChoiceField(queryset=ToReachSemiFinalOutcome.objects.all().order_by('team'),
                                                   required=True,
                                                   widget=forms.RadioSelect,
                                                   label="To reach the semi final")
    to_reach_final_bet = NameModelChoiceField(queryset=ToReachFinalOutcome.objects.all().order_by('team'),
                                              required=True,
                                              widget=forms.RadioSelect,
                                              label="To reach the final")
    to_win_bet = NameModelChoiceField(queryset=ToWinOutcome.objects.all().order_by('team'),
                                      required=True,
                                      widget=forms.RadioSelect,
                                      label="To win the Euros")
    highest_scoring_team_bet = NameModelChoiceField(queryset=HighestScoringTeamOutcome.objects.all().order_by('team'),
                                                    required=True,
                                                    widget=forms.RadioSelect,
                                                    label="Highest scoring team")
    most_yellow_cards_bet = NameModelChoiceField(queryset=MostYellowCardsOutcome.objects.all().order_by('team'),
                                                 required=True,
                                                 widget=forms.RadioSelect,
                                                 label="Most yellow cards")
    fastest_yellow_card_bet = NameModelChoiceField(queryset=FastestYellowCardsOutcome.objects.all().order_by('team'),
                                                   required=True,
                                                   widget=forms.RadioSelect,
                                                   label="Fastest yellow card")
    fastest_tournament_goal_bet = NameModelChoiceField(queryset=FastestGoalOutcome.objects.all().order_by('team'),
                                                       required=True,
                                                       widget=forms.RadioSelect,
                                                       label="Fastest Euro goal")

    class Meta:
        model = BestTeamsSuccessBetGroup
        exclude = ('entry',)


class FiftyFiftyOutcomeForm(forms.Form):
    question1_bet = NameModelChoiceField(queryset=fifty_fifty_questions[0].fiftyfiftyoutcome_set.order_by('-outcome'),
                                         required=True,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[0])
    question2_bet = NameModelChoiceField(queryset=fifty_fifty_questions[1].fiftyfiftyoutcome_set.order_by('-outcome'),
                                         required=True,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[1])
    question3_bet = NameModelChoiceField(queryset=fifty_fifty_questions[2].fiftyfiftyoutcome_set.order_by('-outcome'),
                                         required=True,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[2])
    question4_bet = NameModelChoiceField(queryset=fifty_fifty_questions[3].fiftyfiftyoutcome_set.order_by('-outcome'),
                                         required=True,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[3])
    question5_bet = NameModelChoiceField(queryset=fifty_fifty_questions[4].fiftyfiftyoutcome_set.order_by('-outcome'),
                                         required=True,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[4])
    question6_bet = NameModelChoiceField(queryset=fifty_fifty_questions[5].fiftyfiftyoutcome_set.order_by('-outcome'),
                                         required=True,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[5])
    question7_bet = NameModelChoiceField(queryset=fifty_fifty_questions[6].fiftyfiftyoutcome_set.order_by('-outcome'),
                                         required=True,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[6])
    question8_bet = NameModelChoiceField(queryset=fifty_fifty_questions[7].fiftyfiftyoutcome_set.order_by('-outcome'),
                                         required=True,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[7])
    question9_bet = NameModelChoiceField(queryset=fifty_fifty_questions[8].fiftyfiftyoutcome_set.order_by('-outcome'),
                                         required=True,
                                         widget=forms.RadioSelect,
                                         label=fifty_fifty_questions[8])

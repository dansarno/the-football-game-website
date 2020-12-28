from django import forms
from .models import GroupMatch, TournamentBetGroup, TournamentGoalsOutcome, \
    TournamentOwnGoalsOutcome, TournamentHattricksOutcome, TournamentRedCardsOutcome, FinalBetGroup, \
    FinalFirstGoalOutcome, FinalRefContinentOutcome, FinalGoalsOutcome, FinalYellowCardsOutcome, FinalOwnGoalOutcome


all_matches = GroupMatch.objects.all()


class NameModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.winning_amount}'


class GroupMatchOutcomeForm(forms.Form):
    match1 = NameModelChoiceField(queryset=all_matches[0].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=all_matches[0])
    match2 = NameModelChoiceField(queryset=all_matches[1].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=all_matches[1])
    match3 = NameModelChoiceField(queryset=all_matches[2].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=all_matches[2])
    match4 = NameModelChoiceField(queryset=all_matches[3].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=all_matches[3])
    match5 = NameModelChoiceField(queryset=all_matches[4].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=all_matches[4])
    match6 = NameModelChoiceField(queryset=all_matches[5].groupmatchoutcome_set.all().order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=all_matches[5])


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

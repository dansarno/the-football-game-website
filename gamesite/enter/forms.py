from django import forms
from .models import GroupMatch, GroupMatchOutcome, TournamentBetGroup, TournamentGoalsOutcome, \
    TournamentOwnGoalsOutcome, TournamentHattricksOutcome, TournamentRedCardsOutcome


class NameModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.winning_amount}'


class GroupMatchOutcomeForm(forms.Form):
    match1 = NameModelChoiceField(queryset=GroupMatchOutcome.objects.filter(match_id=1).order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=GroupMatch.objects.get(pk=1))
    match2 = NameModelChoiceField(queryset=GroupMatchOutcome.objects.filter(match_id=2).order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=GroupMatch.objects.get(pk=2))
    match3 = NameModelChoiceField(queryset=GroupMatchOutcome.objects.filter(match_id=3).order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=GroupMatch.objects.get(pk=3))
    match4 = NameModelChoiceField(queryset=GroupMatchOutcome.objects.filter(match_id=4).order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=GroupMatch.objects.get(pk=4))
    match5 = NameModelChoiceField(queryset=GroupMatchOutcome.objects.filter(match_id=5).order_by('-outcome'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=GroupMatch.objects.get(pk=5))


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

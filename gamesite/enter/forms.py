from django import forms
from .models import GroupMatch, GroupMatchOutcome


class NameModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.winning_amount}'


class GroupMatchOutcomeForm(forms.Form):
    match1 = NameModelChoiceField(queryset=GroupMatchOutcome.objects.filter(match_id=1).order_by('-result'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=GroupMatch.objects.get(pk=1))
    match2 = NameModelChoiceField(queryset=GroupMatchOutcome.objects.filter(match_id=2).order_by('-result'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=GroupMatch.objects.get(pk=2))
    match3 = NameModelChoiceField(queryset=GroupMatchOutcome.objects.filter(match_id=3).order_by('-result'),
                                  required=True,
                                  widget=forms.RadioSelect,
                                  label=GroupMatch.objects.get(pk=3))

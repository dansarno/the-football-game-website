from django import forms
from .models import GroupMatch, GroupMatchOutcome


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

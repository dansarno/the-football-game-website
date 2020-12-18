from django import forms
from .models import GroupMatch, GroupMatchOutcome


class GroupMatchForm(forms.ModelForm):
    class Meta:
        model: GroupMatch


class GroupMatchOutcomeForm(forms.Form):
    outcomes = forms.ModelChoiceField(queryset=GroupMatchOutcome.objects.none())

    def __init__(self, match):
        super(GroupMatchOutcomeForm, self).__init__()
        self.fields['outcomes'].queryset = match.groupmatchoutcome_set.all

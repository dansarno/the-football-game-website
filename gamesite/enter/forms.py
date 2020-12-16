from django import forms
from .models import GroupMatch, GroupMatchOutcome


class GroupMatchForm(forms.ModelForm):
    class Meta:
        model: GroupMatch


class GroupMatchOutcomeForm(forms.ModelForm):
    class Meta:
        model = GroupMatchOutcome
        exclude = ('match',)

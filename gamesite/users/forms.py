from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Profile, AccessCode
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from datetime import datetime
from django.conf import settings


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=8)
    first_name = forms.CharField(max_length=10)
    last_name = forms.CharField(max_length=10)
    email = forms.EmailField()
    access_code = forms.CharField(max_length=10, validators=[
                                  RegexValidator(r'^\d{1,10}$')])

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', 'access_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['access_code'].help_text = "An access code is required to create an account."
        self.fields['username'].help_text = "A short unique username, 8 characters max."

    def clean_first_name(self, *args, **kwargs):
        first_name = self.cleaned_data.get("first_name")
        return first_name.title()

    def clean_last_name(self, *args, **kwargs):
        last_name = self.cleaned_data.get("last_name")
        return last_name.title()

    def clean_access_code(self, *args, **kwargs):
        access_code = self.cleaned_data.get("access_code")
        # could use a get and try/except block here
        valid_code = AccessCode.objects.filter(code=access_code).first()
        if not valid_code:
            raise forms.ValidationError("This is not a valid access code")
        elif valid_code.remaining <= 0:
            raise forms.ValidationError("This access code has expired")
        return access_code


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField(max_length=8)
    first_name = forms.CharField(max_length=10)
    last_name = forms.CharField(max_length=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['bio'].widget.attrs.update(rows='2', id="bio-text")
        self.fields['team'].help_text = "Want to create you own team? Get in touch, let us know your team name and your team will be created for you and your friends"
        self.fields['bio'].help_text = "160 characters max"
        if datetime.now() > settings.GAME_DEADLINE:
            self.fields['team'].widget.attrs['disabled'] = True

    class Meta:
        model = Profile
        fields = ['profile_picture', 'team', 'bio']

    def clean_team(self):
        instance = getattr(self, 'instance', None)
        if datetime.now() > settings.GAME_DEADLINE:
            return instance.team
        else:
            return self.cleaned_data['team']

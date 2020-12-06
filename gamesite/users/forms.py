from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import Profile, AccessCode


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    access_code = forms.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'access_code']

    def clean_access_code(self, *args, **kwargs):
        access_code = self.cleaned_data.get("access_code")
        valid_code = AccessCode.objects.filter(code=access_code).first()
        if not valid_code:
            raise forms.ValidationError("This is not a valid access code")
        elif valid_code.remaining <= 0:
            raise forms.ValidationError("This access code has expired")
        valid_code.remaining -= 1
        valid_code.save()
        return access_code


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['profile_picture']

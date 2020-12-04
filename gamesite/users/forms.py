from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    access_code = forms.CharField(max_length=6, validators=[RegexValidator(r'^\d{1,10}$')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'access_code']

    def clean_access_code(self, *args, **kwargs):
        access_code = self.cleaned_data.get("access_code")
        if not access_code == "123456":
            raise forms.ValidationError("This is not a valid access code")
        return access_code

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    team_name = forms.CharField(required=True)
    nation = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'team_name', 'nation']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
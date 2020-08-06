from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(forms.ModelForm):
    """サインアップフォーム"""

    class Meta:
        model = User
        fields = ['username', 'password']
        # widget = {'password': forms.PasswordInput}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'describe', 'image']

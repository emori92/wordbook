from django import forms
# from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(forms.ModelForm):
    """サインアップフォーム"""

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'})
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['describe', 'image']

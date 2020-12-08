from django import forms
from .models import User


class SignupForm(forms.ModelForm):
    """サインアップフォーム"""

    class Meta:
        model = User
        fields = ['username', 'password']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['username'].widget.attrs = {'autofocus': 'autofocus'}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['describe', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['describe'].widget.attrs = {
            'autofocus': 'autofocus',
            'placeholder': '中学生です。よろしくお願いします!\n(80文字まで)',
        }

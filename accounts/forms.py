from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class MyUserCreationForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'password1', 'password2')

    # username = forms.CharField(
    #     label='ユーザー',
    #     widget=forms.PasswordInput(attrs={'placeholder': 'なまえ'})
    # )
    # password1 = forms.CharField(
    #     label='パスワード',
    #     widget=forms.PasswordInput(),
    # )
    # password2 = forms.CharField(
    #     label='パスワード（確認用）',
    #     widget=forms.PasswordInput(),
    # )


class SignupForm(forms.ModelForm):
    """サインアップフォーム"""

#     username = forms.CharField(label='ユーザー:')
#     password = forms.CharField(label='パスワード:', widget=forms.PasswordInput)
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['password'].widget = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['username', 'password']

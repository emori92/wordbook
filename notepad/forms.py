from django import forms
from .models import User, Note


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'describe']
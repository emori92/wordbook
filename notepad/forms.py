from django import forms
from .models import Note, Question


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'describe', 'public']


class TagForm(forms.Form):
    name = forms.CharField(max_length=32)


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'hint', 'answer']

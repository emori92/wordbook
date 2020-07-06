from django import forms
from .models import Note, Question


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'describe', 'public']
        
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['query', 'hint', 'answer']

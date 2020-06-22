from django import forms
from .models import User, Note, Question


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'describe']
        
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['query', 'hint', 'answer']


# フォームにタグを追加
NoteFormSet = forms.inlineformset_factory(
    User,
    Note,
    fields=('title', 'describe'),
    form=NoteForm,
    extra=1,
)
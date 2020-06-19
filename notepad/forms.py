from django import forms
from .models import User, Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'describe']


# フォームにタグを追加
NoteFormSet = forms.inlineformset_factory(
    User,
    Note,
    fields=('title', 'describe'),
    form=NoteForm,
    extra=1,
)
from django import forms
from .models import Note, Question


class SearchForm(forms.Form):
    search = forms.CharField(max_length = 150, label='検索', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['search'].widget.attrs = {
            'autofocus': 'autofocus',
            'placeholder': '検索',
            'class': 'form-control form-control-lg rounded-pill px-4',
            'id': 'search-field',
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'describe', 'public']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'autofocus': 'autofocus'}


class TagForm(forms.Form):
    name = forms.CharField(max_length=32, label='タグ')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'autofocus': 'autofocus'}


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'hint', 'answer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget.attrs = {'autofocus': 'autofocus'}

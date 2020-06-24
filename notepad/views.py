from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import logging

from .models import Note, Question
from .forms import NoteForm, NoteFormSet, QuestionForm

from django.contrib.auth.views import LoginView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


# logging
logger = logging.getLogger(__name__)


# index
class Index(generic.TemplateView):
    template_name = 'notepad/index.html'


# login
class Login(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_url = 'notepad:dashboard'
    success_message = 'Login success!'


# dashboard
class DashBoard(LoginRequiredMixin, generic.ListView):
    model = Note
    template_name = "notepad/dashboard.html"


# note
class NewNoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Note
    formclass = NoteForm
    fields = ['title', 'describe']
    template_name = "notepad/note_new.html"
    success_url = '/dashboard/'
    
    # form_validでユーザーを追加
    def form_valid(self, form):
        
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class NoteDetailView(LoginRequiredMixin, generic.DetailView):
    model = Note
    template_name = "notepad/note_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # noteに紐づくqueryを全て取得
        queryset = Question.objects.filter(note=self.kwargs['pk']).order_by('created_at')
        # queryset = Question.objects.filter(note=self.kwargs.get('pk')).order_by('created_at')
        context['queryset'] = queryset
        return context


class NoteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Note
    formclass = NoteForm
    fields = ['title', 'describe']
    template_name = "notepad/note_new.html"
    success_url = '/dashboard/'


# question
class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Question
    formclass = QuestionForm
    fields = ['query', 'hint', 'answer']
    template_name = "notepad/query_new.html"

    def get_success_url(self):
        # return reverse('notepad:note_detail', kwargs={'pk': self.kwargs['pk']})
        return reverse('notepad:note_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        
        # kwargsの取得
        note = get_object_or_404(Note, pk=self.kwargs.get('pk'))
        form.instance.note = note
        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Question
    formclass = QuestionForm
    fields = ['query', 'hint', 'answer']
    template_name = "notepad/query_new.html"

    def get_success_url(self):
    # def get_success_url(self, note_pk):
        return reverse('notepad:note_detail', kwargs={'pk': self.object.pk})




# View.as_view()
index = Index.as_view()
login = Login.as_view()
dashboard = DashBoard.as_view()
note_new = NewNoteCreateView.as_view()
note_detail = NoteDetailView.as_view()
note_edit = NoteUpdateView.as_view()
query_new = QuestionCreateView.as_view()
query_edit = QuestionUpdateView.as_view()
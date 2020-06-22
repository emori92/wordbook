from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import logging

from .models import Note, Question
from .forms import NoteForm, NoteFormSet, QuestionForm

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View, TemplateView, RedirectView, FormView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


# logging
logger = logging.getLogger(__name__)

class Index(TemplateView):
    template_name = 'notepad/index.html'


class Login(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_url = 'notepad:dashboard'
    success_message = 'Login success!'


class DashBoard(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    
    model = Note
    template_name = "notepad/dashboard.html"


class NewNoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'describe']
    template_name = "notepad/new_note.html"
    formclass = NoteForm
    success_url = '/dashboard/'
    
    # form_validでユーザーを追加
    def form_valid(self, form):
        
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)


class NoteDetailView(LoginRequiredMixin, DetailView):
    model = Note
    template_name = "notepad/note_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # noteに紐づくqueryを全て取得
        queryset = Question.objects.filter(note=self.kwargs['pk']).order_by('created_at')
        # queryset = Question.objects.filter(note=self.kwargs.get('pk')).order_by('created_at')
        context['queryset'] = queryset
        return context


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['query', 'hint', 'answer']
    template_name = "notepad/new_query.html"
    formclass = QuestionForm

    def get_success_url(self):
        # return reverse('notepad:note_detail', kwargs={'pk': self.kwargs['pk']})
        return reverse('notepad:note_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        
        # kwargsの取得
        note = get_object_or_404(Note, pk=self.kwargs.get('pk'))
        form.instance.note = note
        return super().form_valid(form)


index = Index.as_view()
login = Login.as_view()
dashboard = DashBoard.as_view()
new_note = NewNoteCreateView.as_view()
note_detail = NoteDetailView.as_view()
new_query = QuestionCreateView.as_view()
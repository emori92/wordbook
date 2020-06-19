from django.shortcuts import render, redirect
from django.urls import reverse
import logging

from .models import Note
from .forms import NoteForm, NoteFormSet

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



index = Index.as_view()
login = Login.as_view()
dashboard = DashBoard.as_view()
new_note = NewNoteCreateView.as_view()
note_detail = NoteDetailView.as_view()
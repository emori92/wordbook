from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Note
from .forms import NoteForm

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View, TemplateView, RedirectView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin



class Index(TemplateView):
    template_name = 'notepad/index.html'

index = Index.as_view()


class Login(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_url = '/dashboard/'
    success_message = 'Login success!'

login = Login.as_view()


class DashBoard(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    
    model = Note
    template_name = "notepad/dashboard.html"

dashboard = DashBoard.as_view()


class NewNote(LoginRequiredMixin, FormView):
    template_name = 'notepad/new_note.html'
    form_class = NoteForm
    success_url = '/new_note/'

new_note = NewNote.as_view()
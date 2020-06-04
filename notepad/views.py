from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Note

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import View, TemplateView, RedirectView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


class Index(TemplateView):
    template_name = 'notepad/index.html'

index = Index.as_view()


class Login(LoginView, SuccessMessageMixin):
    template_name = 'registration/login.html'
    success_url = '/dashboard/'
    success_message = 'Done Login!'

login = Login.as_view()


class DashBoardListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    
    model = Note
    template_name = "notepad/dashboard.html"

dashboard = DashBoardListView.as_view()
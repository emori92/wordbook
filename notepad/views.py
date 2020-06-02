from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.generic import View, TemplateView, RedirectView, FormView, ListView
from .models import Note
from .forms import LoginForm


class Index(TemplateView):
    template_name = 'notepad/index.html'

index = Index.as_view()



class DashBoard(ListView):
    model = Note
    template_name = "notepad/dashboard.html"

dashboard = DashBoard.as_view()
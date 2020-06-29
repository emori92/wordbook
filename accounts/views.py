from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
# view
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin

from .models import User
from .forms import MyUserCreationForm, SignupForm


# login
class Login(SuccessMessageMixin, LoginView):
    template_name = 'accounts/login.html'
    success_message = 'Login success!'


# signup
class SignupView(CreateView):
    model = User
    formclass = SignupForm
    fields = ['username', 'password']
    template_name = "accounts/signup.html"
    success_url = reverse_lazy('notepad:dashboard')

    def form_valid(self, form, request):
        # ユーザー登録
        self.object = form.save(commit=False)
        username = self.object.username
        self.object.set_password(self.object.password)
        self.object = form.save()
        # ログイン
        # password = self.object.password
        # user = authenticate(username=username, password=password)
        # login(request, user)
        
        return super().form_valid(form)

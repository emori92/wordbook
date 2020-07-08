from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
# view
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin

from .models import User
from .forms import MyUserCreationForm, SignupForm, ProfileForm


# login
class Login(SuccessMessageMixin, LoginView):
    template_name = 'accounts/login.html'
    success_message = 'Login success!'


# signup
class SignupView(generic.CreateView):
    model = User
    formclass = SignupForm
    template_name = "accounts/signup.html"
    fields = ['username', 'password']
    success_url = reverse_lazy('notepad:dashboard')

    def form_valid(self, form):
        # ユーザー取得
        self.object = form.save(commit=False)
        username = form.cleaned_data.get('username')
        # パスワードハッシュ化
        self.object.set_password(form.cleaned_data.get('password'))
        self.object = form.save()
        # ログイン
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)


# profile
class ProfileUpdateView(generic.UpdateView):
    model = User
    formclass = ProfileForm
    template_name = "accounts/profile.html"

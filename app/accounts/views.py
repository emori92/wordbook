from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
# view
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin

from .models import User
from .forms import SignupForm, ProfileForm


# login
class LoginView(SuccessMessageMixin, LoginView):
    template_name = 'accounts/login.html'
    success_message = 'ログインしました！'
    
    def get_success_url(self):
        return reverse('notepad:dashboard', kwargs={'pk': self.request.user.pk})

    # ログインしている場合マイページにリダイレクト
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            return HttpResponseRedirect(reverse('notepad:dashboard', kwargs={'pk': user.pk}))
        else:
            return super().get(request, *args, **kwargs)


# sign up
class SignupView(generic.CreateView):
    model = User
    form_class = SignupForm
    template_name = "accounts/signup.html"
    
    def get_success_url(self):
        return reverse('notepad:dashboard', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        # ユーザー取得
        self.object = form.save(commit=False)
        data = form.cleaned_data
        username = data.get('username')
        # パスワード登録
        password = data.get('password')
        self.object.set_password(password)
        self.object = form.save()
        # ログイン
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)

    # ログインしている場合マイページにリダイレクト
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            return HttpResponseRedirect(reverse('notepad:dashboard', kwargs={'pk': user.pk}))
        else:
            return super().get(request, *args, **kwargs)


# profile
class ProfileUpdateView(generic.UpdateView):
    model = User
    formclass = ProfileForm
    fields = ['describe', 'image']
    template_name = "accounts/profile.html"

    def get_success_url(self):
        return reverse('notepad:dashboard', kwargs={'pk': self.request.user.pk})

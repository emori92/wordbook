from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
# view
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User, Follow
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


# login by tutorial user
class TutorialLoginView(generic.RedirectView):
    """Tutorial Userでログイン"""

    def get_redirect_url(self, *args, **kwargs):
        # user info
        username = 'TutorialUser'
        password = 'HelloWordbook'
        # login
        tutorial_user = authenticate(username=username, password=password)
        login(self.request, tutorial_user)
        # redirect dashboard
        pk = self.request.user.pk
        url = reverse('notepad:dashboard', kwargs={'pk': pk})
        return url


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


# SNS
class FollowView(LoginRequiredMixin, generic.RedirectView):
    login_url = '/login/'

    # リダイレクト先
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs['followed']
        url = reverse('notepad:dashboard', kwargs={'pk': pk})
        return url

    # フォロー、フォロー削除
    def get(self, request, *args, **kwargs):
        # フォローするユーザーとされるユーザーを取得
        following = User.objects.get(pk=self.kwargs['following'])
        followed = User.objects.get(pk=self.kwargs['followed'])
        # pkをDBに格納 or 削除
        if Follow.objects.filter(following=following, followed=followed).exists():
            follow = Follow.objects.get(following=following, followed=followed)
            follow.delete()
        else:
            follow = Follow.objects.create(following=following, followed=followed)
            follow.save()
        return super().get(request, *args, **kwargs)

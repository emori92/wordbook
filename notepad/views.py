from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import logging

from accounts.models import User
from .models import Note, Question, Follow
from .forms import NoteForm, QuestionForm

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


# logging
logger = logging.getLogger(__name__)


# index
class Index(generic.TemplateView):
    template_name = 'notepad/index.html'


class RankingListView(generic.ListView):
    model = Note
    template_name = "notepad/ranking.html"
    
def get_queryset(self):
    queryset = super().get_queryset()
    return Note.objects.filter(public=1)

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context


class HotListView(generic.ListView):
    model = Note
    template_name = "notepad/hot.html"

    def get_queryset(self):
        # return Note.objects.filter(public=1).order_by('-created_at')[:60]  # 本番用
        return Note.objects.filter().order_by('-created_at')[:60]  # 60件まで取得
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 推薦されたノートをcontextに追加
        # demo_query = Note.objects.filter()
        demo_query = Note.objects.filter(public=1)  # 本番用
        context['recommender'] = demo_query
        return context


# dashboard
class Dashboard(generic.ListView):
    model = Note
    template_name = "notepad/dashboard.html"

    # ユーザー取得
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # dashboardに表示するUser取得
        context['account'] = User.objects.get(pk=self.kwargs['pk'])
        # フォローするユーザーとされるユーザーを取得
        following = User.objects.get(pk=self.request.user.pk)
        followed = User.objects.get(pk=self.kwargs['pk'])
        # フォローの有無
        follow_state = Follow.objects.filter(following=following, followed=followed).exists()
        print(f'\n\n{follow_state}\n\n')
        context['follow_state'] = follow_state
        return context

    # ユーザーの単語帳を取得
    def get_queryset(self):
        return Note.objects.filter(user=self.kwargs['pk']).order_by('-updated_at')


class FollowView(LoginRequiredMixin, generic.RedirectView):
    # url = '/dashboard/'
    pattern_name = 'notepad:dashboard'
    # query_string = True

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
    
    def get_redirect_url(self, *args, **kwargs):
        url = '/dashboard/%s/' % self.kwargs['following']
        return url


# note
class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Note
    formclass = NoteForm
    fields = ['title', 'describe', 'public']
    template_name = "notepad/note_new.html"
    # success_url = '/dashboard/'
    
    # form_validでユーザーを追加
    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super().form_valid(form)

    def get_success_url(self):
        note_pk = self.object.pk
        return reverse('notepad:note_detail', kwargs={'pk': note_pk})


class NoteDetailView(generic.DetailView):
    model = Note
    template_name = "notepad/note_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # noteに紐づくqueryを全て取得
        queryset = Question.objects.filter(note=self.kwargs['pk']).order_by('-updated_at')
        context['queryset'] = queryset
        return context


class NoteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Note
    formclass = NoteForm
    fields = ['title', 'describe', 'public']
    template_name = "notepad/note_new.html"
    
    def get_success_url(self):
        note_pk = self.object.pk
        return reverse('notepad:note_detail', kwargs={'pk': note_pk})


class NoteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Note
    template_name = 'notepad/note_delete.html'
    success_url = '/dashboard/'


# question
class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Question
    formclass = QuestionForm
    fields = ['query', 'hint', 'answer']
    template_name = "notepad/query_new.html"

    def get_success_url(self):
        note_pk = self.object.note_id
        return reverse('notepad:note_detail', kwargs={'pk': note_pk})

    def form_valid(self, form):
        # kwargsのpk取得
        note = get_object_or_404(Note, pk=self.kwargs.get('pk'))
        form.instance.note = note
        return super().form_valid(form)


class QuestionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Question
    formclass = QuestionForm
    fields = ['query', 'hint', 'answer']
    template_name = "notepad/query_new.html"

    def get_success_url(self):
        pk = self.object.note_id
        return reverse('notepad:note_detail', kwargs={'pk': pk})


class QuestionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Question
    template_name = "notepad/query_delete.html"

    def get_success_url(self):
        pk = self.object.note_id
        return reverse('notepad:note_detail', kwargs={'pk': pk})

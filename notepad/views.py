from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from django.db.models import Count
import logging

from accounts.models import User
from .models import Note, Question, Follow, Star
from .forms import NoteForm, QuestionForm
from SQL.notepad import hot_query  # SQL query

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
        # いいねされたノートをランキング形式で取得
        note = Note.objects.filter(public=1, star__gt=0).values('id', 'title', 'describe', 'user_id', 'user__username') \
            .annotate(star_num=Count('star__id')).order_by('-star_num')
        return note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # フォロー数の多い人を抽出
        users = User.objects.filter(followed__followed__gt=0).values('id', 'username', 'describe') \
            .annotate(user_num=Count('followed__followed')).order_by('-user_num')
        context['users'] = users
        return context


class HotListView(generic.ListView):
    model = Note
    template_name = "notepad/hot.html"

    def get_queryset(self):
        # 新規投稿を取得
        return Note.objects.filter(public=1).order_by('-created_at')[:60]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # フォローしているユーザーのノートを取得
        if self.request.user.is_authenticated:
            note = Note.objects.raw(hot_query, [self.request.user.pk])
            context['follow_note'] = note
        # 推薦されたノートを取得
        demo_query = Note.objects.filter()  # デモデータ
        context['recommender'] = demo_query
        return context


# dashboard
class Dashboard(generic.ListView):
    model = Note
    template_name = "notepad/dashboard.html"

    # ユーザーの単語帳を取得
    def get_queryset(self):
        return Note.objects.filter(user=self.kwargs['pk']).order_by('-updated_at')

    # ユーザー取得
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # dashboardに表示するUser取得
        context['account'] = User.objects.get(pk=self.kwargs['pk'])
        # フォローするユーザーとされるユーザーを取得
        if self.request.user.is_authenticated:
            following = User.objects.get(pk=self.request.user.pk)
            followed = User.objects.get(pk=self.kwargs['pk'])
            # ユーザーがフォローしているか真偽値を取得
            follow_state = Follow.objects.filter(following=following, followed=followed).exists()
            context['follow_state'] = follow_state
        # 公開されている単語帳のみ取得
        public_list = Note.objects.filter(user=self.kwargs['pk'], public=1).order_by('-updated_at')
        context['public_list'] = public_list
        # いいねした単語帳を取得
        if self.request.user.pk == self.kwargs['pk']:
            liked_note = Note.objects.filter(star__user=self.request.user.pk)
            context['liked_note'] = liked_note
        return context


# note
class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Note
    formclass = NoteForm
    fields = ['title', 'describe', 'public']
    template_name = "notepad/note_new.html"
    
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
        # いいねの判定
        if self.request.user.is_authenticated:
            # 単語帳とユーザーを特定
            note = Note.objects.get(pk=self.kwargs['pk'])
            user = User.objects.get(pk=self.request.user.pk)
            # いいねの有無を真偽値で格納
            star_state = Star.objects.filter(note=note, user=user).exists()
            context['star_state'] = star_state
        # いいね数
        star_num = Star.objects.filter(note_id=self.kwargs['pk'])
        # starテーブルにレコードの有無を確認（レコードがないとエラーになるので、定数0を格納）
        if star_num.exists():
            context['star_num'] = star_num.values('note_id').annotate(num=Count('id')).get(note_id=self.kwargs['pk'])
        else:
            context['star_num'] = {'num': 0}
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

    def get_success_url(self):
        note_pk = self.object.user_id
        return reverse('notepad:dashboard', kwargs={'pk': note_pk})


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


# SNS
class FollowView(LoginRequiredMixin, generic.RedirectView):
    # リダイレクト先
    def get_redirect_url(self, *args, **kwargs):
        url = '/dashboard/%s/' % self.kwargs['followed']
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


class StarView(LoginRequiredMixin, generic.RedirectView):
    # リダイレクト先
    def get_redirect_url(self, *args, **kwargs):
        url = '/note/%s/' % self.kwargs['note_pk']
        return url

    def get(self, request, *args, **kwargs):
        # いいねするユーザーと、いいねされる単語帳を取得
        user = User.objects.get(pk=self.kwargs['user_pk'])
        note = Note.objects.get(pk=self.kwargs['note_pk'])
        # DBに登録 or 削除
        if Star.objects.filter(user=user, note=note).exists():
            liked_note = Star.objects.get(user=user, note=note)
            liked_note.delete()
        else:
            liked_note = Star.objects.create(user=user, note=note)
            liked_note.save()
        return super().get(request, *args, **kwargs)
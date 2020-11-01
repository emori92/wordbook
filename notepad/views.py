from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
import logging

from accounts.models import User
from .models import Note, Question, Review, Follow, Star, Tag
from .forms import SearchForm, NoteForm, QuestionForm, TagForm
# paginator
from config.my_module.views_functions import set_ranking, set_paginator, set_ranking_num

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


# logging
logger = logging.getLogger(__name__)


page_num = 12


# home
class HomeView(generic.TemplateView):
    template_name = 'notepad/index.html'

    # ログインしている場合マイページにリダイレクト
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            return HttpResponseRedirect(reverse('notepad:dashboard', kwargs={'pk': user.pk}))
        else:
            return super().get(request, *args, **kwargs)


class RankingListView(generic.ListView):
    model = Note
    template_name = "notepad/ranking.html"
    paginate_by = page_num
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # いいねされた数が多いノートを降順で取得
        note = Note.objects.select_related('user') \
            .filter(public=1, star__gt=0) \
            .annotate(star_num=Count('star__id')).order_by('-star_num', 'title')
        return note

    # いいね、ユーザー、タグのランキング情報をcontextに代入
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # いいね
        stars_query = self.get_queryset()
        set_ranking(self, context, stars_query, 'page', 'stars', 'ranking_stars')
        # フォロー
        users_query = User.objects.prefetch_related('followed') \
            .filter(followed__followed__gt=0) \
            .annotate(followed_num=Count('followed__followed')) \
            .order_by('-followed_num')
        set_ranking(self, context, users_query, 'user', 'users', 'ranking_users')
        # タグ
        tags_query = Tag.objects.all() \
            .annotate(tag_num=Count('note__id')) \
            .filter(tag_num__gt=0).order_by('-tag_num')
        set_ranking(self, context, tags_query, 'tag', 'tags', 'ranking_tags')
        return context


class HotListView(generic.ListView):
    model = Note
    template_name = "notepad/hot.html"
    paginate_by = 12

    def get_queryset(self):
        # 新規投稿を取得
        note = Note.objects.select_related('user') \
            .filter(public=1) \
            .annotate(star_num=Count('star__id')).order_by('-created_at')
        return note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # フォローしているユーザーのノートを取得
        if self.request.user.is_authenticated:
            # フォローしているuserを取得
            pk = self.request.user.pk
            user_id = Follow.objects.filter(following_id=pk).values('followed_id')
            users = User.objects.filter(id__in=user_id)
            # フォローしているuserのnoteを取得
            note = Note.objects.filter(public=1, user__in=users).select_related('user')
            context['follow'] = set_paginator(self, note, 'follow', page_num=100)
        # 推薦されたノートを取得
        recommender_query = Note.objects.select_related('user') \
            .filter(public=1).annotate(star_num=Count('star__id'))
        context['recommender'] = set_paginator(self, recommender_query, 'recommender')
        return context


class SearchView(generic.FormView):
    model = Note
    form_class = SearchForm
    template_name = "notepad/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 単語帳/単語帳/タグを取得
        wordbook = Note.objects.select_related('user').filter(public=1)
        user = User.objects
        tag = Tag.note_set.through.objects.values('tag', 'tag__name')
        # 検索用語を取得
        word = self.request.GET.get('search')
        # 検索している場合の処理
        if word:
            wordbook = wordbook.annotate(star_num=Count('star__id')) \
                .filter(title__icontains=word).order_by('-created_at', 'title')
            user = user.filter(username__icontains=word) \
                .annotate(follow_num=Count('followed__id')).order_by('-follow_num', 'username')
            tag = tag.filter(tag__name__icontains=word) \
                .annotate(tag_num=Count('id')).order_by('-tag_num', 'tag')
        # 検索してない場合の処理
        else:
            wordbook = wordbook.annotate(star_num=Count('star__id')) \
                .order_by('-created_at', 'title')
            user = user.annotate(follow_num=Count('followed__id')) \
                .order_by('-follow_num', 'username')
            tag = tag.annotate(tag_num=Count('id')).order_by('-tag_num', 'tag')
        # contextに単語帳、ユーザー、タグを登録
        context['wordbook'] = set_paginator(self, wordbook, 'page')
        context['user'] = set_paginator(self, user, 'user')
        context['tag'] = set_paginator(self, tag, 'tag')
        return context


# dashboard
class Dashboard(generic.ListView):
    model = Note
    template_name = "notepad/dashboard.html"
    paginate_by = 12

    # ユーザーの単語帳を取得
    def get_queryset(self):
        return Note.objects.filter(user=self.kwargs['pk']) \
            .annotate(star_num=Count('star__id')).order_by('-updated_at') \
            .select_related('user')

    # ユーザー取得
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # dashboardに表示するUser取得
        dashboard_query = User.objects.get(pk=self.kwargs['pk'])
        context['account'] = dashboard_query
        # フォローするユーザーとされるユーザーを取得
        if self.request.user.is_authenticated:
            following = User.objects.get(pk=self.request.user.pk)
            followed = dashboard_query
            # ユーザーがフォローしているか真偽値を取得
            # この真偽値で、templateの「フォロー」「フォロー解除」の表示を切り替える
            follow_state = Follow.objects.filter(
                following=following, followed=followed) \
                .select_related('note__id').exists()
            context['follow_state'] = follow_state
        # 公開されている単語帳のみ取得
        # 自分以外のユーザーには公開情報を表示
        public = Note.objects.filter(user=self.kwargs['pk'], public=1) \
            .annotate(star_num=Count('star__id')).order_by('-updated_at')
        context['public'] = set_paginator(self, public, 'public')
        # いいねした単語帳を取得
        if self.request.user.pk == self.kwargs['pk']:
            liked = Note.objects.filter(
                star__user=self.request.user.pk, public=1) \
                .annotate(star_num=Count('star__id')).select_related('user')
            context['liked'] = set_paginator(self, liked, 'liked')
        return context


# note
class NoteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Note
    formclass = NoteForm
    fields = ['title', 'describe', 'public']
    template_name = "notepad/note_new.html"
    login_url = '/login/'

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
        # noteに紐づくquestionを全て取得
        note_pk = self.kwargs['pk']
        queryset = Question.objects.filter(note=note_pk) \
            .prefetch_related('review_set').order_by('created_at')
        context['queryset'] = set_paginator(self, queryset, 'page')
        # 復習ボタンの表示切り替えを判別するリストを作成
        review_query = Review.objects.select_related('question') \
            .filter(question__note_id=note_pk)
        review_judge = [(r.question_id, r.user_id) for r in review_query]
        context['review_judge'] = review_judge
        # ブラウザで復習一覧を表示するquerysetを作成
        review_list = Question.objects.prefetch_related('review_set').filter(
            note=note_pk, review__user_id=self.request.user.pk)
        context['review_list'] = set_paginator(self, review_list, 'review')
        # いいねの判定
        if self.request.user.is_authenticated:
            # 単語帳とユーザーを特定
            note = Note.objects.get(pk=note_pk)
            user = User.objects.get(pk=self.request.user.pk)
            # いいねの有無を真偽値で格納
            star_state = Star.objects.filter(note=note, user=user).exists()
            context['star_state'] = star_state
        # いいね数
        star_num = Star.objects.filter(note_id=note_pk)
        # starテーブルにレコードの有無を確認（レコードがないとエラーになるので定数0を格納）
        if star_num.exists():
            context['star_num'] = star_num.values('note_id') \
                .annotate(num=Count('id')).get(note_id=note_pk)
        else:
            context['star_num'] = {'num': 0}
        return context


class NoteUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Note
    formclass = NoteForm
    fields = ['title', 'describe', 'public']
    template_name = "notepad/note_update.html"
    login_url = '/login/'

    def get_success_url(self):
        note_pk = self.object.pk
        return reverse('notepad:note_detail', kwargs={'pk': note_pk})


class NoteDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Note
    template_name = 'notepad/note_delete.html'
    login_url = '/login/'

    def get_success_url(self):
        note_pk = self.object.user_id
        return reverse('notepad:dashboard', kwargs={'pk': note_pk})


# tag
class TagCreateView(LoginRequiredMixin, generic.FormView):
    template_name = 'notepad/tag_new.html'
    form_class = TagForm
    login_url = '/login/'

    def get_success_url(self):
        note_pk = self.kwargs['note_pk']
        url = reverse('notepad:note_detail', kwargs={'pk': note_pk})
        return url

    def form_valid(self, form):
        # tagの取得 or 作成
        text = form.cleaned_data['name']
        tag, created = Tag.objects.get_or_create(name=text)
        # noteに紐付ける
        note_pk = self.kwargs['note_pk']
        note = get_object_or_404(Note, id=note_pk)
        note.tag.add(tag)
        return super().form_valid(form)


class TagListView(generic.ListView):
    model = Note
    template_name = "notepad/tag_list.html"

    # タグ付けされたnoteのみ取得
    def get_queryset(self):
        keyword = self.kwargs['word']
        tags = Note.objects.select_related('user') \
            .filter(tag__name=keyword, public=1) \
            .annotate(star_num=Count('star__id'))
        queryset = set_paginator(self, tags, 'tag')
        return queryset


class TagDeleteListView(LoginRequiredMixin, generic.ListView):
    template_name = "notepad/tag_delete.html"
    login_url = '/login/'

    # ノートに紐づいたタグを取得
    def get_queryset(self):
        queryset = Note.objects.get(id=self.kwargs['note_pk']) \
            .tag.filter(note=self.kwargs['note_pk'])
        return queryset


class TagDeleteView(LoginRequiredMixin, generic.RedirectView):
    login_url = '/login/'

    # リダイレクト先のURL
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs['note_pk']
        url = reverse('notepad:tag_delete_list', kwargs={'note_pk': pk})
        return url

    # タグの削除
    def get(self, request, *args, **kwargs):
        # noteの取得
        note = Note.objects.get(id=self.kwargs['note_pk'])
        # tagの取得
        tag = Tag.objects.get(name=self.kwargs['tag'])
        # tag削除
        note.tag.remove(tag)
        return super().get(request, *args, **kwargs)


# question
class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Question
    formclass = QuestionForm
    fields = ['question', 'hint', 'answer']
    template_name = "notepad/question_new.html"
    login_url = '/login/'

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
    fields = ['question', 'hint', 'answer']
    template_name = "notepad/question_new.html"
    login_url = '/login/'

    def get_success_url(self):
        pk = self.object.note_id
        return reverse('notepad:note_detail', kwargs={'pk': pk})


class QuestionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Question
    template_name = "notepad/question_delete.html"
    login_url = '/login/'

    def get_success_url(self):
        pk = self.object.note_id
        return reverse('notepad:note_detail', kwargs={'pk': pk})


class QuestionReviewView(LoginRequiredMixin, generic.RedirectView):
    login_url = '/login/'

    # 問題の復習を確認する
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs['note_pk']
        url = reverse('notepad:note_detail', kwargs={'pk': pk})
        return url

    def get(self, request, *args, **kwargs):
        # pkを定義
        q_id = self.kwargs['question_pk']
        u_id = self.request.user.pk
        # pkからユーザーのreviewを取得
        queryset = Review.objects.filter(question_id=q_id, user_id=u_id)
        # querysetが空であればレコード作成
        if queryset.exists():
            review_query = queryset.get(user_id=u_id)
            review_query.delete()
        else:
            review_query = Review.objects.create(question_id=q_id, user_id=u_id)
            review_query.save()
        return super().get(request, *args, **kwargs)


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


class StarView(LoginRequiredMixin, generic.RedirectView):
    login_url = '/login/'

    # リダイレクト先
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs['note_pk']
        url = reverse('notepad:note_detail', kwargs={'pk': pk})
        return url

    def get(self, request, *args, **kwargs):
        # いいねするユーザーと、いいねされる単語帳を取得
        user = User.objects.get(pk=self.kwargs['user_pk'])
        note = Note.objects.get(pk=self.kwargs['note_pk'])
        # DBに登録 or 削除
        if Star.objects.filter(user=user, note=note).exists():
            star = Star.objects.get(user=user, note=note)
            star.delete()
        else:
            star = Star.objects.create(user=user, note=note)
            star.save()
        return super().get(request, *args, **kwargs)

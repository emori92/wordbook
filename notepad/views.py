from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
import logging

from accounts.models import User
from .models import Note, Question, Review, Follow, Star, Tag
from .forms import SearchForm, NoteForm, QuestionForm, TagForm
# SQL query
from .SQL.user_follow_query import hot_query
# paginator
from .my_script.views_functions import set_paginator, set_ranking_num

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


# logging
logger = logging.getLogger(__name__)


# home
class Index(generic.TemplateView):
    template_name = 'notepad/index.html'

    # ログインしている場合マイページにリダイレクト
    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            user_pk = self.request.user.pk
            return HttpResponseRedirect(reverse('notepad:dashboard', kwargs={'pk': user_pk}))
        else:
            super().post(request, *args, **kwargs)


class RankingListView(generic.ListView):
    model = Note
    template_name = "notepad/ranking.html"
    paginate_by = 4
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # いいねされた数が多いノートを降順で取得
        note = Note.objects.filter(public=1, star__gt=0).select_related('user') \
            .annotate(star_num=Count('star__id')).order_by('-star_num')
        return note

    # いいね、ユーザー、タグのランキング情報をcontextに代入
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # いいね、フォロワー、タグで共通の処理を関数化
        def set_ranking(queryset, url_name, queryset_name, ranking_objects_name):
            object_list = set_paginator(self, queryset, url_name)
            context[queryset_name] = object_list
            context[ranking_objects_name] = set_ranking_num(object_list)

        # いいね
        stars_query = self.get_queryset()
        set_ranking(stars_query, 'page', 'stars', 'ranking_stars')
        # フォロー
        users_query = User.objects.filter(followed__followed__gt=0) \
            .annotate(followed_num=Count('followed__followed')).order_by('-followed_num')
        set_ranking(users_query, 'user', 'users', 'ranking_users')
        # タグ
        tags_query = Tag.objects.all() \
            .annotate(tag_num=Count('note__id')) \
            .filter(tag_num__gt=0).order_by('-tag_num')
        set_ranking(tags_query, 'tag', 'tags', 'ranking_tags')
        return context


class HotListView(generic.ListView):
    model = Note
    template_name = "notepad/hot.html"
    paginate_by = 4

    def get_queryset(self):
        # 新規投稿を取得
        note = Note.objects.filter(public=1) \
            .annotate(star_num=Count('star__id')).order_by('-created_at')
        return note

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # フォローしているユーザーのノートを取得
        if self.request.user.is_authenticated:
            # "/notepad/SQL/"にあるクエリ文を実行
            note = Note.objects.raw(hot_query, [self.request.user.pk])
            context['follow'] = set_paginator(self, note, 'follow')
        # 推薦されたノートを取得
        demo_query = Note.objects.annotate(star_num=Count('star__id'))  # デモデータ
        context['recommender'] = set_paginator(self, demo_query, 'recommender')
        return context


class SearchView(generic.FormView):
    model = Note
    form_class = SearchForm
    template_name = "notepad/search.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 検索用語を取得
        word = self.request.GET.get('search')
        # 検索用語から該当する単語帳を取得
        wordbook = Note.objects.filter(public=1)
        user = User.objects
        tag = Tag.objects
        if word:
            wordbook = wordbook.annotate(star_num=Count('star__id')) \
                .filter(title__icontains=word).order_by('-created_at')
            user = user.filter(username__icontains=word)
            tag = tag.filter(name__icontains=word)
        else:
            wordbook = wordbook.annotate(star_num=Count('star__id')) \
                .order_by('-created_at')
            user = user.all()
            tag = tag.all()
        # contextに単語帳、ユーザー、タグを登録
        context['wordbook'] = set_paginator(self, wordbook, 'wordbook')
        context['users'] = set_paginator(self, user, 'user')
        context['tags'] = set_paginator(self, tag, 'tag')
        return context


# dashboard
class Dashboard(generic.ListView):
    model = Note
    template_name = "notepad/dashboard.html"
    paginate_by = 4

    # ユーザーの単語帳を取得
    def get_queryset(self):
        return Note.objects.filter(user=self.kwargs['pk']) \
            .annotate(star_num=Count('star__id')).order_by('-updated_at')

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
            # この真偽値で、templateの「フォロー」「フォロー解除」の表示を切り替える
            follow_state = Follow.objects.filter(following=following, followed=followed).exists()
            context['follow_state'] = follow_state
        # 公開されている単語帳のみ取得
        # 自分以外のユーザーには公開情報を表示
        public = Note.objects.filter(user=self.kwargs['pk'], public=1) \
            .annotate(star_num=Count('star__id')).order_by('-updated_at')
        context['public'] = set_paginator(self, public, 'public')
        # いいねした単語帳を取得
        if self.request.user.pk == self.kwargs['pk']:
            liked = Note.objects.filter(star__user=self.request.user.pk) \
                .annotate(star_num=Count('star__id'))
            context['liked'] = set_paginator(self, liked, 'liked')
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
        # noteに紐づくquestionを全て取得
        queryset = Question.objects.filter(note=self.kwargs['pk']) \
            .prefetch_related('review_set').order_by('created_at')
        context['queryset'] = queryset
        # 復習ボタンの表示切り替えを判別するタプルを作成
        review_query = Review.objects.select_related('question') \
            .filter(question__note_id=self.kwargs['pk'])
        review_tuple = [(r.question_id, r.user_id) for r in review_query]
        context['review_tuple'] = review_tuple
        # ブラウザで復習一覧を表示するquerysetを作成
        review_list = Question.objects.prefetch_related('review_set') \
            .filter(note=self.kwargs['pk'], review__user_id=self.request.user.pk)
        context['review_list'] = review_list
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
        # starテーブルにレコードの有無を確認（レコードがないとエラーになるので定数0を格納）
        if star_num.exists():
            context['star_num'] = star_num.values('note_id') \
                .annotate(num=Count('id')).get(note_id=self.kwargs['pk'])
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


# tag
class TagCreateView(LoginRequiredMixin, generic.FormView):
    template_name = 'notepad/tag_new.html'
    form_class = TagForm

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
        tags = Note.objects.prefetch_related('tag') \
            .filter(tag__name=keyword, public=1) \
            .annotate(star_num=Count('star__id'))
        queryset = set_paginator(self, tags, 'tag')
        return queryset


class TagDeleteListView(LoginRequiredMixin, generic.ListView):
    template_name = "notepad/tag_delete.html"

    # ノートに紐づいたタグを取得
    def get_queryset(self):
        queryset = Note.objects.get(id=self.kwargs['note_pk']) \
            .tag.filter(note=self.kwargs['note_pk'])
        return queryset

    # note_pkをcontextに登録
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['note_pk'] = self.kwargs['note_pk']
        return context


class TagDeleteView(LoginRequiredMixin, generic.RedirectView):
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

    def get_success_url(self):
        pk = self.object.note_id
        return reverse('notepad:note_detail', kwargs={'pk': pk})


class QuestionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Question
    template_name = "notepad/question_delete.html"

    def get_success_url(self):
        pk = self.object.note_id
        return reverse('notepad:note_detail', kwargs={'pk': pk})


class QuestionReviewView(LoginRequiredMixin, generic.RedirectView):
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
            liked_note = Star.objects.get(user=user, note=note)
            liked_note.delete()
        else:
            liked_note = Star.objects.create(user=user, note=note)
            liked_note.save()
        return super().get(request, *args, **kwargs)

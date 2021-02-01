from django.urls import path
from . import views


app_name = 'notepad'

urlpatterns = [
    # base
    path('', views.HomeView.as_view(), name='home'),
    path('ranking/', views.RankingListView.as_view(), name='ranking'),
    path('hot/', views.HotListView.as_view(), name='hot'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('dashboard/<int:pk>/', views.Dashboard.as_view(), name='dashboard'),
    # note
    path('note/', views.NoteCreateView.as_view(), name='note_new'),
    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('note/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note_edit'),
    path('note/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
    # tag
    path('tag/<int:note_pk>/', views.TagCreateView.as_view(), name='tag_new'),
    path('tag/<str:word>/', views.TagListView.as_view(), name='tag_list'),
    path('tag/<int:note_pk>/delete/', views.TagDeleteListView.as_view(), name='tag_delete_list'),
    path('tag/<int:note_pk>/<str:tag>/', views.TagDeleteView.as_view(), name='tag_delete'),
    # question
    path('note/<int:pk>/question/', views.QuestionCreateView.as_view(), name='question_new'),
    path('question/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='question_edit'),
    path('question/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('question/<int:note_pk>/<int:question_pk>/<int:user_pk>/', views.QuestionReviewView.as_view(), name='question_review'),
    # SNS
    path('star/<int:note_pk>/<int:user_pk>/', views.StarView.as_view(), name='star'),
]

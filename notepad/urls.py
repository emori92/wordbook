from django.urls import path
from . import views


app_name = 'notepad'

urlpatterns = [
    # base
    path('', views.Index.as_view(), name='index'),
    # path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('dashboard/<int:pk>/', views.Dashboard.as_view(), name='dashboard'),
    # path('test/', views.FollowView.as_view(), name='follow'),
    path('<int:following>/<int:followed>/', views.FollowView.as_view(), name='follow'),
    # note
    path('note_new/', views.NoteCreateView.as_view(), name='note_new'),
    path('note/<int:pk>/', views.NoteDetailView.as_view(), name='note_detail'),
    path('note/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note_edit'),
    path('note/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),
    # query
    path('note/<int:pk>/query_new/', views.QuestionCreateView.as_view(), name='query_new'),
    path('query/<int:pk>/edit/', views.QuestionUpdateView.as_view(), name='query_edit'),
    path('query/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='query_delete'),
    # ranking hot
    path('ranking/', views.RankingListView.as_view(), name='ranking'),
    path('hot/', views.HotListView.as_view(), name='hot'),
]
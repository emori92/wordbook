from django.urls import path
from . import views


app_name = 'notepad'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # note
    path('note_new/', views.note_new, name='note_new'),
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
    path('note/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
    # query
    path('note/<int:pk>/query_new/', views.query_new, name='query_new'),
    path('query/<int:pk>/edit/', views.query_edit, name='query_edit'),
    path('query/<int:pk>/delete/', views.query_delete, name='query_delete'),
]
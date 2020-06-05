from django.urls import path
from . import views


app_name = 'notepad'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('new_note/', views.new_note, name='new_note'),
]
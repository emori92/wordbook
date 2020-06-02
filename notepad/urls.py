from django.urls import path
from . import views


app_name = 'notepad'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashbord', views.dashboard, name='dashboard')
]
from django.urls import path

from django.contrib.auth.views import LogoutView
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile'),
]
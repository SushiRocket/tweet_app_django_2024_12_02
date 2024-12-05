from django.urls import path
from.views import IndexView,SignUpView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('tweet_create/', views.tweet_create, name='tweet_create'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('tweet_detail/<int:pk>/', views.tweet_detail, name='tweet_detail'),
    path('tweet_edit/<int:pk>/', views.tweet_edit, name='tweet_edit'),
    path('tweet_delete/<int:pk>/', views.tweet_delete, name='tweet_delete'),
    path('like_toggle/<int:pk>/', views.like_toggle,name='like_toggle'),

    #認証関連
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app/logout.html'), name='logout'),
]
from django.urls import path
from.views import IndexView,SignUpView
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('tweet_create/', views.tweet_create, name='tweet_create'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('tweet_detail/<int:pk>/', views.tweet_detail, name='tweet_detail'),
    path('tweet_edit/<int:pk>/', views.tweet_edit, name='tweet_edit'),
    path('tweet_delete/<int:pk>/', views.tweet_delete, name='tweet_delete'),
    path('tweet/<int:pk>/like/', views.like_toggle,name='like_toggle'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('user/<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:pk>/reply/',views.add_reply, name='add_reply'),
    path('search/', views.tweet_search, name='tweet_search'),

    #認証関連
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='app/logout.html'), name='logout'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'), # Твоя новая функция
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='shopapp/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('game/<int:game_id>/', views.game_detail_view, name='game_detail'),
]
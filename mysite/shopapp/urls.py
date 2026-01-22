from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'), # Твоя новая функция
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='shopapp/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('game/<int:game_id>/', views.game_detail_view, name='game_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'), # Новая строка
    path('favorite/add/<int:game_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorite/remove/<int:game_id>/', views.remove_from_favorites, name='remove_from_favorites'),
]
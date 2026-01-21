from django.contrib import admin

from .models import User, Game, GameCatalog, Player

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'release_year', 'rating')
    search_fields = ('title', 'genre')

@admin.register(GameCatalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('catalog_name', 'created_at')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'role', 'is_active')

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'user')

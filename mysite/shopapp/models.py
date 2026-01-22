from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver


# --- Менеджер для кастомного пользователя ---
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'administrator')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# --- Таблица "Пользователь" (users) ---
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('administrator', 'Администратор'),
        ('player', 'Игрок'),
    ]
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='player')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'

# --- Таблица "Компьютерные игры" (computer_games) ---
class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    release_year = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        db_table = 'computer_games'

    def __str__(self):
        return self.title

# --- Таблица "Каталоги игр" (game_catalogs) ---
class GameCatalog(models.Model):
    catalog_id = models.AutoField(primary_key=True)
    catalog_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Связь многие-ко-многим через твою таблицу
    games = models.ManyToManyField(Game,through='CatalogGame', related_name='in_catalogs')

    class Meta:
        db_table = 'game_catalogs'

# --- Промежуточная таблица "Игры в каталогах" (catalog_games) ---
class CatalogGame(models.Model):
    catalog = models.ForeignKey(GameCatalog, on_delete=models.CASCADE, db_column='catalog_id')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, db_column='game_id')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'catalog_games'
        unique_together = (('catalog', 'game'),)

# --- Таблица "Игрок" (players) ---
class Player(models.Model):
    player_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')
    nickname = models.CharField(max_length=100, unique=True)
    avatar_url = models.URLField(max_length=500, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Избранные игры через твою таблицу
    favorite_games = models.ManyToManyField(Game, through='PlayerFavoriteGame', related_name='favorited_by')

    class Meta:
        db_table = 'players'

# --- Промежуточная таблица "Любимые игры" (player_favorite_games) ---
class PlayerFavoriteGame(models.Model):
    # Django автоматически создаст поле id, если его нет,
    # но так как мы его добавили в БД, просто оставляем как есть.
    player = models.ForeignKey(Player, on_delete=models.CASCADE, db_column='player_id')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, db_column='game_id')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'player_favorite_games'
        # Это важно для Django:
        unique_together = (('player', 'game'),)

@receiver(post_save, sender=User)
def create_player_profile(sender, instance, created, **kwargs):
    if created:
        # Создаем игрока автоматически при создании пользователя
        Player.objects.get_or_create(
            user=instance,
            defaults={'nickname': instance.email.split('@')[0]}
        )
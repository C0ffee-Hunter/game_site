from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm
from django.db.models import Q # Импортируем Q для сложного поиска
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm
from .forms import PlayerProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Game, User, Player


# Главная страница (Каталог)
def index_view(request):
    query = request.GET.get('q', '')
    if query:
        games = Game.objects.filter(title__icontains=query)
    else:
        games = Game.objects.all()
    return render(request, 'shopapp/index.html', {'games': games, 'query': query})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Так как мы указали USERNAME_FIELD = 'email' в модели,
        # authenticate будет проверять email.
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Перенаправляем на главную
        else:
            # Если данные неверны, передаем ошибку в шаблон
            return render(request, 'shopapp/login.html', {
                'error': 'Неверный e-mail или пароль'
            })

    return render(request, 'shopapp/login.html')

# Регистрация
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # 1. Сохраняем пользователя (но не в БД сразу, чтобы захешировать пароль)
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Хешируем пароль
            user.role = 'player'  # Устанавливаем роль по умолчанию
            user.save()  # Теперь сохраняем в таблицу users

            # 3. Автоматически логиним пользователя после регистрации
            login(request, user)
            return redirect('profile')  # Перенаправляем в личный кабинет
        else:
            print(form.errors)
            form = RegistrationForm()
    else:
        form = RegistrationForm()

    return render(request, 'shopapp/register.html', {'form': form})


# Профиль
@login_required
def profile_view(request):
    # Получаем профиль текущего игрока
    #player = Player.objects.get(user=request.user)
    #return render(request, 'shopapp/profile.html', {'player': player})
    player, created = Player.objects.get_or_create(
        user=request.user,
        defaults={'nickname': request.user.email.split('@')[0]}  # временный ник из почты
    )
    return render(request, 'accounts/profile.html', {'player': player})

@login_required
def add_to_favorites(request, game_id):
    if request.method == 'POST':
        game = get_object_or_404(Game, game_id=game_id)
        # Получаем профиль игрока для текущего юзера
        player = request.user.player
        # Добавляем игру в ManyToMany поле favorite_games
        player.favorite_games.add(game)
        return redirect('profile') # Или обратно на страницу игры
    return redirect('index')

# Выход
def logout_view(request):
    logout(request)
    return redirect('index')


def game_detail_view(request, game_id): # <--- Проверьте это имя!
    game = get_object_or_404(Game, game_id=game_id)
    return render(request, 'shopapp/game_detail.html', {'game': game})


def index_view(request):
    # Получаем текст из поля ввода (name="q")
    query = request.GET.get('q', '').strip()
    genre_query = request.GET.get('genre', '').strip()

    games = Game.objects.all()

    if query:
        # Ищем игру по названию ИЛИ по жанру
        games = games.filter(
            Q(title__icontains=query)
        )
    else:
        # Если поиска нет — показываем все игры
        games = Game.objects.all()

    if genre_query:
        # Используем iexact для точного совпадения (без учета регистра)
        games = games.filter(genre__iexact=genre_query)

    return render(request, 'shopapp/index.html', {
        'games': games,
        'query': query,
        'genre_selected': genre_query  # Передаем, чтобы сохранить выбор в выпадающем списке
    })


# Просмотр профиля
@login_required
def profile_view(request):
    # Получаем игрока, связанного с текущим пользователем
    player = get_object_or_404(Player, user=request.user)
    return render(request, 'shopapp/profile.html', {'player': player})


# Редактирование профиля
@login_required
def edit_profile(request):
    player = get_object_or_404(Player, user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Возвращаемся в профиль после сохранения
    else:
        form = ProfileEditForm(instance=player)

    return render(request, 'shopapp/edit_profile.html', {'form': form})


@login_required
def edit_profile_view(request):
    # Получаем профиль игрока, привязанного к текущему пользователю
    player = get_object_or_404(Player, user=request.user)

    if request.method == 'POST':
        # Заполняем форму данными из запроса и привязываем к существующему объекту player
        form = PlayerProfileForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('profile')  # После сохранения отправляем на страницу профиля
    else:
        # Если это просто переход на страницу — показываем форму с текущими данными
        form = PlayerProfileForm(instance=player)

    return render(request, 'shopapp/profile_edit.html', {'form': form})


# Добавление в избранное
@login_required
def add_to_favorites(request, game_id):
    if request.method == 'POST': # Обрабатываем только нажатие кнопки
        game = get_object_or_404(Game, game_id=game_id)
        request.user.player.favorite_games.add(game)
    return redirect(request.META.get('HTTP_REFERER', 'index'))

@login_required
def remove_from_favorites(request, game_id):
    if request.method == 'POST': # Обрабатываем только нажатие кнопки
        game = get_object_or_404(Game, game_id=game_id)
        request.user.player.favorite_games.remove(game)
    return redirect(request.META.get('HTTP_REFERER', 'profile'))


# Проверка: является ли пользователь администратором
def is_admin(user):
    return user.is_authenticated and user.role == 'administrator'


@user_passes_test(is_admin)
def admin_dashboard(request):
    games = Game.objects.all().order_by('-game_id')
    users = User.objects.all().order_by('-user_id')

    context = {
        'games': games,
        'users': users,
        'total_games': games.count(),
        'total_users': users.count(),
    }
    return render(request, 'shopapp/admin_dashboard.html', context)


@user_passes_test(is_admin)
def admin_delete_game(request, game_id):
    game = get_object_or_404(Game, game_id=game_id)
    game.delete()
    return redirect('admin_dashboard')


@user_passes_test(is_admin)
def admin_delete_user(request, user_id):
    # Не даем админу удалить самого себя
    if request.user.user_id != user_id:
        user_to_delete = get_object_or_404(User, user_id=user_id)
        user_to_delete.delete()
    return redirect('admin_dashboard')
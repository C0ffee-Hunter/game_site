from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Game, Player, User
from .forms import RegistrationForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Game
from django.db.models import Q # Импортируем Q для сложного поиска


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
            # Создаем пользователя
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            # Создаем связанный профиль игрока
            Player.objects.create(user=user, nickname=form.cleaned_data['nickname'])
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'shopapp/register.html', {'form': form})

# Профиль
@login_required
def profile_view(request):
    # Получаем профиль текущего игрока
    player = Player.objects.get(user=request.user)
    return render(request, 'shopapp/profile.html', {'player': player})

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
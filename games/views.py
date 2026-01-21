from django.shortcuts import render

def index(request):
    # Тестовый список игр (имитация базы данных)
    dummy_games = [
        {
            'id': 1,
            'title': 'The Witcher 3',
            'genre': 'RPG',
            'publisher': 'CD Projekt',
            'year': 2015,
            'rating': 9.8,
        },
        {
            'id': 2,
            'title': 'Cyberpunk 2077',
            'genre': 'Action RPG',
            'publisher': 'CD Projekt',
            'year': 2020,
            'rating': 8.5,
        },
        {
            'id': 3,
            'title': 'Elden Ring',
            'genre': 'Souls-like',
            'publisher': 'Bandai Namco',
            'year': 2022,
            'rating': 9.5,
        },
    ]
    return render(request, 'shopapp/index.html', {'shopapp': dummy_games})

def game_detail(request, game_id):
    # Имитируем получение одной игры по ID
    game = {
        'id': game_id,
        'title': 'The Witcher 3',
        'genre': 'RPG',
        'publisher': 'CD Projekt',
        'country': 'Польша',
        'year': 2015,
        'rating': 9.8,
        'description': 'Легендарная игра про ведьмака Геральта в открытом мире.'
    }
    return render(request, 'shopapp/game_detail.html', {'game': game})

def profile(request):
    # Имитируем данные игрока
    player = {
        'nickname': 'SuperGamer_2024',
        'email': 'player@example.com',
        'role': 'Игрок',
        'favorite_games': [
            {'id': 1, 'title': 'The Witcher 3'},
            {'id': 2, 'title': 'Cyberpunk 2077'}
        ]
    }
    return render(request, 'shopapp/profile.html', {'player': player})

def login_view(request):
    return render(request, 'shopapp/login.html')

def register_view(request):
    return render(request, 'shopapp/register.html')
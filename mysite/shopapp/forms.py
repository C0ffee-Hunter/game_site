from .models import User, Player
from django import forms
from .models import Game

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Повторите пароль")
    nickname = forms.CharField(label="Никнейм")

    class Meta:
        model = User
        fields = ('email', 'password')


    def clean_password_confirm(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password_confirm')
        if p1 != p2:
            raise forms.ValidationError("Пароли не совпадают")
        return p2

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['nickname', 'bio', 'avatar_url']
        labels = {
            'nickname': 'Ваш никнейм',
            'bio': 'О себе',
            'avatar_url': 'Ссылка на аватар'
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Расскажите о себе...'}),
        }

class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['nickname', 'avatar_url', 'bio'] # Поля, которые можно менять
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-input'}),
            'avatar_url': forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
        }
        labels = {
            'nickname': 'Никнейм (псевдоним)',
            'avatar_url': 'Ссылка на аватар',
            'bio': 'О себе',
        }


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'genre', 'publisher', 'country', 'release_year', 'rating']
        widgets = {
            field: forms.TextInput(attrs={'class': 'admin-input'}) for field in ['title', 'genre', 'publisher', 'country']
        }
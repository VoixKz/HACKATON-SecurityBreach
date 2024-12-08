from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import EmailValidator, RegexValidator
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        validators=[EmailValidator(message="Введите корректный адрес электронной почты.")],
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=150,
        required=False,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message="Имя пользователя может содержать только буквы, цифры и символы @/./+/-/_."
        )],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким адресом электронной почты уже существует.")
        return email


class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        required=True,
        validators=[EmailValidator(message="Введите корректный адрес электронной почты.")],
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
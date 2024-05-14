from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms

from user.models import User


class UserSignUpForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', required=True, widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': 'Имя пользователя'}))

    password1 = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput(
        attrs={'type': 'password', 'placeholder': 'Пароль'}))

    password2 = forms.CharField(label='Повторите пароль', required=True, widget=forms.PasswordInput(
        attrs={'type': 'password', 'placeholder': 'Повторите пароль'}))

    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': 'Фамилия'}))
    email = forms.CharField(label='Email', required=True, widget=forms.EmailInput(
        attrs={'type': 'text', 'placeholder': 'Email'}))

    # confirm_password = forms.CharField(label='Подтвердите пароль', required=True, widget=forms.PasswordInput(
    #     attrs={'type': 'password', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class UserSignInForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', required=True, widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput(
        attrs={'type': 'password', 'placeholder': 'Пароль'}))

    __user = None

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username', '')
        password = cleaned_data.get('password', '')

        self.__user = authenticate(username=username, password=password)

        if self.__user is None:
            raise ValidationError('Неверное имя пользователя или пароль.')

        return cleaned_data

    def get_user(self):
        return self.__user

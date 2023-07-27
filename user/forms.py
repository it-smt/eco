import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.exceptions import ValidationError

from .models import User


class SignUpForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    middle_name = forms.CharField(label='Отчество (если есть)', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    number = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'aria-describedby': 'basic-addon1'
    }))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    status = forms.ChoiceField(label='Статус пользователя', choices=User.Status.choices, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name', 'username',
                  'number', 'email', 'status', 'password1', 'password2')

    def clean_number(self):
        number = self.cleaned_data['number']
        if not re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', number):
            raise ValidationError('Некорректный номер телефона.')

        return number


class SignInForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


class ChangeUserInfoForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    middle_name = forms.CharField(label='Отчество (если есть)', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    number = forms.CharField(label='Номер телефона', widget=forms.TextInput(attrs={
        'class': 'form-control'

    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'middle_name',
                  'username', 'number')

    def clean_number(self):
        number = self.cleaned_data['number']
        if not re.match(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', number):
            raise ValidationError('Некорректный номер телефона.')

        return number


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    new_password2 = forms.CharField(label='Подтверждение нового пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(label='Почта', max_length=254, widget=forms.EmailInput(
        attrs={'autocomplete': 'email', 'class': 'form-control'}))


class PasswordSetForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label='Подтвердите новый пароль',
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )


class ConfirmEmailForm(forms.Form):
    code = forms.IntegerField(label='Код подтверждения', widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))


class ChangeEmailForm(forms.ModelForm):
    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('email',)

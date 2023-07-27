from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpRequest, request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, logout, login
from django.core.mail import send_mail

from .forms import ChangeUserInfoForm, SignUpForm, SignInForm, ChangePasswordForm, ConfirmEmailForm, ChangeEmailForm
from .confirmation import generate_code

import config


class UserLoginView(LoginView):
	"""Класс-представление входа пользователя."""
	template_name = 'user/login.html'
	form_class = SignInForm


class UserLogoutView(LoginRequiredMixin, LogoutView):
	"""Класс-представление выхода пользователя."""
	template_name = 'user/logout.html'


@login_required
def profile(request):
	"""Функция-представление профиля пользователя."""
	return render(request, 'user/profile.html')


def register(request):
	"""Функция-представление регистрации пользователя."""
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('user:send_code_email')
	else:
		form = SignUpForm()
	context = {'form': form}
	return render(request, 'user/register.html', context)


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
	"""Класс-представление изменения пароля."""
	template_name = 'user/change_password/index.html'
	form_class = ChangePasswordForm
	success_url = reverse_lazy('user:login')
	success_message = 'Ваш пароль успешно изменен!'

	def form_valid(self, form):
		logout(self.request)
		form.save()
		update_session_auth_hash(self.request, form.user)
		return super().form_valid(form)


@login_required
def change_user_info(request):
	"""Фкнция-представление изменения данных пользователя."""
	if request.method == 'POST':
		form = ChangeUserInfoForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, 'Ваши данные успешно изменены!')
			return redirect('user:profile')
	else:
		form = ChangeUserInfoForm(instance=request.user)
	context = {'form': form}
	return render(request, 'user/change_info/index.html', context)


def confirm_email(request):
	"""Функция-представление подтверждения почты."""
	user = request.user
	if user.is_email_confirmed:
		messages.error(request, 'Ваша почта уже подтверждена!')
		return redirect('user:profile')
	else:
		if request.method == 'POST':
			form = ConfirmEmailForm(request.POST)
			if form.is_valid():
				print(request.POST.get('code'), user.code, type(
					request.POST.get('code')), type(user.code))
				if request.POST.get('code') == user.code:
					user.is_email_confirmed = True
					user.save()
					messages.success(request, 'Почта успешно подтверждена!')
					return redirect('user:profile')
				else:
					messages.error(
						request, 'Неверный код! Попробуйте еще раз.')
		else:
			form = ConfirmEmailForm()
		context = {
			'form': form
		}
		return render(request, 'user/confirm_email/index.html', context)


def send_code_email(request):
	"""Функция-представление отправки кода подтверждения."""
	user = request.user
	if user.is_email_confirmed:
		messages.error(request, 'Ваша почта уже подтверждена!')
		return redirect('user:profile')
	else:
		try:
			code = generate_code()
			send_mail('Код подтверждения',
					  f'Здравствуйте, {user.first_name}!\n\nВаш код для подтверждения почты: {code}.\n\nС уважением, Администрация сайта Чистый Мир', config.EMAIL_HOST_USER, [user.email])
			user.code = code
			user.save()
			return redirect('user:confirm_email')
		except Exception:
			messages.error(
				request, 'Проблема при отправке сообщения! Проверьте ваше интернет-соединение и повторите попытку позже.')
			user.delete()
			return redirect('user:register')


def change_email(request):
	"""Функция-представление изменения почты пользователя."""
	user = request.user
	if request.method == 'POST':
		form = ChangeEmailForm(request.POST)
		if form.is_valid():
			user.email = request.POST.get('email')
			user.is_email_confirmed = False
			user.save()
			return redirect('user:send_code_email')
	else:
		form = ChangeEmailForm()
	context = {'form': form}
	return render(request, 'user/change_email/index.html', context)

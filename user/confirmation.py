from random import randint

from django.core.mail import send_mail

import requests

import config
from .models import User


def generate_code() -> int:
	"""Функция генерирует 6-значный код подтверждения.

	Returns:
			int: 6-значный код подтверждения.
	"""
	return randint(100000, 999999)


def send_code_sms(number: str, first_name: str) -> dict:
	"""Функция отправляет сообщение с кодом подтверждения на номер телефона пользователя.

	Args:
					number (str): Номер телефон пользователя.
					first_name (str): Имя пользователя.

	Return:
					response (dict): Ответ API сайта SMS Aero.
	"""
	code = generate_code()
	message = f'Здравствуйте, {first_name}!\n\nВаш код для подтверждения номера телефона: {code}.\n\nАдминистрация сайта Чистый Мир'
	response = requests.get(
		f'https://{config.SMS_AERO_EMAIL}:{config.SMS_AERO_API_KEY}@gate.smsaero.ru/v2/sms/send?number={number}&text={message}&sign=SMS Aero').json()
	return code

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Status(models.TextChoices):
        WORKER = 'Работник', 'Работник'
        CUSTOMER = 'Заказчик', 'Заказчик'

    email = models.EmailField(_("email address"), unique=True)
    middle_name = models.CharField(
        max_length=255, verbose_name='Отчество', blank=True)
    number = models.CharField(max_length=30, verbose_name='Номер телефона')
    status = models.CharField(max_length=10, choices=Status.choices,
                              default=Status.CUSTOMER, verbose_name='Статус пользователя')
    is_email_confirmed = models.BooleanField(
        default=False, verbose_name='Почта подтверждена?')
    code = models.CharField(max_length=6, default='',
                            verbose_name='Последний код подтверждения', blank=True)

    class Meta:
        AbstractUser.Meta
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def is_worker(self):
        return self.status == 'Работник'

    def is_customer(self):
        return self.status == 'Заказчик'

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}' if self.middle_name else f'{self.last_name} {self.first_name}'

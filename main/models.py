from django.db import models
from django.urls import reverse

from user.models import User


class Message(models.Model):
    """Модель Заявки."""

    class Type(models.TextChoices):
        """Класс выбора типа."""
        metal = 'Металл', 'Металл'
        plastic = 'Пластик', 'Пластик'
        technique = 'Техника', 'Техника'
        battery = 'Батарейки', 'Батарейки'

    author = models.ForeignKey(to=User, on_delete=models.CASCADE,
                               verbose_name='Автор', related_name='authors')
    type = models.CharField(
        max_length=80, choices=Type.choices, default=Type.metal, verbose_name='Тип')
    weight = models.FloatField(verbose_name='Вес (примерный в кг)')
    address = models.CharField(
        max_length=500, verbose_name='Адрес, откуда забрать')
    time_s = models.TimeField(verbose_name='Присутствую с')
    time_b = models.TimeField(verbose_name='До')
    is_complited = models.BooleanField(
        default=False, verbose_name='Заявка выполнена?')
    submitted = models.DateTimeField(
        auto_now_add=True, verbose_name='Заявка оставлена')
    worker = models.ForeignKey(to=User, on_delete=models.PROTECT, blank=True,
                               null=True, verbose_name='Исполнитель', related_name='workers')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['-submitted', 'author']

    def __str__(self):
        return f'{self.author.get_full_name()} - {self.type}'

    def worker_is_not_none(self):
        return self.worker is not None

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import Truncator

from .constants import (EMAIL_MAX_LENGTH, ORDER_TITLE_MAX_LENGTH, TRIM_LEN,
                        USERNAME_MAX_LENGTH)
from .validators import date_of_birth_validator, username_validator


class User(AbstractUser):
    username = models.CharField(
        'Логин',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        help_text='Только буквы, цифры и @/./+/-/_',
        validators=[username_validator]
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
    )
    date_of_birth = models.DateField(
        'Дата рождения',
        validators=[date_of_birth_validator]
    )

    def __str__(self):
        return Truncator(self.username).chars(TRIM_LEN)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)


class Order(models.Model):
    title = models.CharField('Наименование', max_length=ORDER_TITLE_MAX_LENGTH)
    description = models.TextField('Описание', blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь'
    )
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    def __str__(self):
        return (f'Заказ #{self.id}: {Truncator(self.title).chars(TRIM_LEN)} '
                f'(пользователь: {self.user})')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        default_related_name = 'orders'
        ordering = ('-updated_at',)

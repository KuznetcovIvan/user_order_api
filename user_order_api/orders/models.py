from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Case, ExpressionWrapper, F, IntegerField, Q, When
from django.db.models.functions import (ExtractDay, ExtractMonth, ExtractYear,
                                        Now)
from django.utils.text import Truncator

from .constants import (DESCRIPTION_MAX_LENGTH, EMAIL_MAX_LENGTH,
                        TITLE_MAX_LENGTH, TRIM_LEN, USERNAME_MAX_LENGTH)
from .validators import birth_date_validator, username_validator


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
    birth_date = models.DateField(
        'Дата рождения',
        validators=[birth_date_validator],
        help_text='Введите дату рождения',
        null=True,
        blank=True
    )

    def __str__(self):
        return Truncator(self.username).chars(TRIM_LEN)

    @staticmethod
    def calculate_age_expression():
        now, birth = Now(), F('birth_date')
        return ExpressionWrapper(
            ExtractYear(now) - ExtractYear(birth)
            - Case(
                When(
                    Q(birth_date__month__gt=ExtractMonth(now))
                    | (Q(birth_date__month=ExtractMonth(now))
                       & Q(birth_date__day__gt=ExtractDay(now))),
                    then=1
                ),
                default=0,
                output_field=IntegerField()
            ),
            output_field=IntegerField()
        )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-date_joined',)


class Order(models.Model):
    title = models.CharField('Наименование', max_length=TITLE_MAX_LENGTH)
    description = models.TextField(
        'Описание', max_length=DESCRIPTION_MAX_LENGTH,
    )
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
        indexes = [models.Index(fields=['user'])]

import re
from datetime import date

from django.conf import settings
from rest_framework.exceptions import ValidationError

from .constants import AGE_MAX_VALUE


def username_validator(username):
    if username == settings.PROFILE_URL_SEGMENT:
        raise ValidationError(
            f'Логин "{settings.PROFILE_URL_SEGMENT}" запрещен.')
    invalid_chars = re.findall(r'[^\w.@+-]', username)
    if invalid_chars:
        raise ValidationError(
            'Недопустимые символы в логине: {} '
            'Разрешены только буквы, цифры и @/./+/-/_'.format(
                ''.join(set(invalid_chars))))
    return username


def date_of_birth_validator(date_of_birth):
    today = date.today()
    age = today.year - date_of_birth.year
    if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
        age -= 1

    if age < 0 or age > AGE_MAX_VALUE:
        raise ValidationError(
            'Дата рождения должна соответствовать возрасту '
            f'от 0 до {AGE_MAX_VALUE} лет.'
        )

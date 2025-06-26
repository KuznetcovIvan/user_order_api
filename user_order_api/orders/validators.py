import re
from datetime import date

from django.conf import settings
from rest_framework.exceptions import ValidationError

from .constants import AGE_MAX_VALUE, PATTERN


def username_validator(username):
    if username == settings.PROFILE_URL_SEGMENT:
        raise ValidationError(
            f'Логин "{settings.PROFILE_URL_SEGMENT}" запрещен.')
    invalid_chars = re.findall(PATTERN, username)
    if invalid_chars:
        raise ValidationError(
            'Недопустимые символы в логине: {} '
            'Разрешены только буквы, цифры и @/./+/-/_'.format(
                ''.join(set(invalid_chars))))
    return username


def birth_date_validator(birth_date):
    today = date.today()
    if birth_date > today:
        raise ValidationError(
            f'Дата рождения {birth_date} больше текущей даты.'
        )
    if today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    ) > AGE_MAX_VALUE:
        raise ValidationError(
            f'Возраст не может превышать {AGE_MAX_VALUE} лет.'
        )
    return birth_date

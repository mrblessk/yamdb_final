import datetime as dt

from django.core.exceptions import ValidationError


def validate_username(value):
    FORBIDDEN_USERNAME = ['me', 'ME', 'Me', 'mE']
    for name in FORBIDDEN_USERNAME:
        if value == name:
            raise ValidationError(f'Имя {value} использовать нельзя')
    return value


def validate_year(value):
    if value > dt.date.today().year:
        raise ValidationError(
            f'Это произведение Вы сможете добавить в {value} году.'
        )
    return value

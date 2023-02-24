import re

from rest_framework.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Недопустимое имя пользователя')
    pattern = re.compile(r'^[\w.@+-]+$')
    if not pattern.match(value):
        raise ValidationError(
            'Имя пользователя может содержать только буквы, цифры и @/./+/-/_')
    return value


def validate_hex_color(value):
    pattern = re.compile(r'^#[0-9a-fA-F]{6}$')
    if not pattern.match(value):
        raise ValidationError(
            'Некорректный формат цвета')
    return value

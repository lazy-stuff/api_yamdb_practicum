from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator

ADMIN = "Администратор"
MODERATOR = "Модератор"
USER = "Пользователь"


class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""

    roles = (
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (USER, USER)
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=50,
        unique=True,
        validators=[UnicodeUsernameValidator]
    )
    email = models.EmailField('Email', max_length=150, unique=True)
    role = models.CharField(
        verbose_name='Роль пользователя',
        choices=roles,
        max_length=15,
        default='user'
    )
    bio = models.TextField('Биография', max_length=350, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=30,
        null=True
    )

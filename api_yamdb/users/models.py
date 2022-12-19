from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.validators import UnicodeUsernameValidator


class CustomUser(AbstractUser):
    """Кастомная модель пользователя"""

    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'
    USERS_ROLES = (
        (ROLE_USER, 'user'),
        (ROLE_MODERATOR, 'moderator'),
        (ROLE_ADMIN, 'admin'),
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
        choices=USERS_ROLES,
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

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.username

    @property
    def role_is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def role_is_moderator(self):
        return self.role == self.ROLE_MODERATOR

    @property
    def role_is_user(self):
        return self.role == self.ROLE_USER

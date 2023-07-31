from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Модель для пользователя с разными ролями.
    У каждой роли определённый доступ.
    """

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOIСES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.TextField('Роль', choices=ROLE_CHOIСES, default=USER)

    class Meta:
        ordering = ('role',)

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_admin(self):
        return self.role == User.ADMIN

    @property
    def is_user(self):
        return self.role == User.USER

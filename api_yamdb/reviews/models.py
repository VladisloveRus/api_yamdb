from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """Кастомная модель пользователя. Добавлены поля биографии и роли."""
    ROLE_CHOICES = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )

    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        choices=ROLE_CHOICES, default='user', max_length=255
    )

    def __str__(self):
        return self.username

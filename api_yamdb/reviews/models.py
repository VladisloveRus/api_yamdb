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
from .validators import validate_year


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название категории",
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Slug",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название жанра",
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Slug",
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название произведения",
    )
    year = models.IntegerField(
        validators=[validate_year],
        verbose_name="Год произведения",
    )
    description = models.TextField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Описание произведения",
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name="titles",
        verbose_name="Жанр произведения",
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name="Категория произведения",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_year


class CustomUser(AbstractUser):
    """Кастомная модель пользователя. Добавлены поля биографии и роли."""

    ROLE_CHOICES = (
        ("user", "Аутентифицированный пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Администратор"),
    )
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(blank=False, null=True, max_length=32)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        choices=ROLE_CHOICES, default="user", max_length=255
    )

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == "user"

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_admin(self):
        return self.role == "admin"


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
    rating = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Рейтинг произведения",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField(
        verbose_name="Текст отзыва",
    )
    score = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)],
        verbose_name="Оценка",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_author_title",
                fields=["author", "title"],
            )
        ]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
    )
    text = models.TextField(
        verbose_name="Текст комментария",
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата добавления"
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text

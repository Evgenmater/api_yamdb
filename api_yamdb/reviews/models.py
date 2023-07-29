"""Models for YAMDB."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User
from reviews.validators import validate_year


class Category(models.Model):
    """Class Categories."""

    name = models.CharField(
        verbose_name='название',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='идентификатор',
        max_length=200,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)


class Genre(models.Model):
    """Class Genres."""

    name = models.CharField(
        verbose_name='название',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='идентификатор',
        max_length=200,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ('name',)


class Title(models.Model):
    """Class Titles."""

    name = models.CharField(
        verbose_name='название',
        max_length=200
    )
    year = models.IntegerField(
        verbose_name='дата выхода',
        validators=[validate_year]
    )
    description = models.TextField(
        verbose_name='описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    rating = models.IntegerField(
        verbose_name='рейтинг',
        null=True,
        default=None
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ('name',)


class GenreTitle(models.Model):
    """Class GenreTitle."""

    title = models.ForeignKey(
        Title,
        verbose_name='произведение',
        on_delete=models.CASCADE)
    genre = models.ForeignKey(
        Genre,
        verbose_name='жанр',
        on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, жанр - {self.genre}'

    class Meta:
        verbose_name = 'произведение и жанр'
        verbose_name_plural = 'произведения и жанры'


class Review(models.Model):
    """Модель для отзывов с рейтингом."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='произведение')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор')
    score = models.IntegerField(
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        verbose_name='оценка')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата публикации')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель для комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='отзыв')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата публикации')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return self.text

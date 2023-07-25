"""Models for YAMDB."""
from django.db import models

from .validators import validate_year


class User():
    """Class User."""
    pass


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
    """Class Reviews."""
    pass


class Comment(models.Model):
    """Class Comments."""
    pass

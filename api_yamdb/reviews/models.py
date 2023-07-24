"""Models for YAMDB."""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User():
    """Class User."""
    pass


class Category(models.Model):
    """Class Categories."""
    pass


class Genre(models.Model):
    """Class Genres."""
    pass


class Title(models.Model):
    """Class Titles."""
    pass


class GenreTitle(models.Model):
    """Class GenreTitle."""

    pass


class Review(models.Model):
    """Class Reviews."""
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
    """Class Comments."""
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

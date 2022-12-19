from django.db import models
from users.models import CustomUser
from titles.models import Title
from django.core.validators import MinValueValidator, MaxValueValidator

from api_yamdb.settings import CONSTANTS


class Review(models.Model):
    """Модель отзывов на произведения"""
    text = models.TextField('Текст отзыва', null=True, blank=True)
    author = models.ForeignKey(
        CustomUser,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='author_review'
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Оценённое произведение',
        on_delete=models.CASCADE,
        related_name='title_review'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, 'Оценка не можыт юыть ниже 1'),
            MaxValueValidator(10, 'Оценка не должна превышать 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.text[:CONSTANTS['LETTERS_PER_POST']]

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]


class Comment(models.Model):
    """Модель комментариев по отзывам"""
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='author_comment'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Комментируемый отзыв',
        related_name='comment_review'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:CONSTANTS['LETTERS_PER_POST']]

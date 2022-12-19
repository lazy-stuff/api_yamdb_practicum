from django.db import models


class Genres(models.Model):
    """Модель для хранения жанров произведений."""

    id = models.AutoField(primary_key=True)
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Псевдоним', max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Categories(models.Model):
    """Модель для хранения категорий произведений."""

    id = models.AutoField(primary_key=True)
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Псевдоним', max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для хранения подробностей о произведении."""

    id = models.AutoField(primary_key=True)
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField(default=0)
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='title',
        verbose_name='Категория',
        null=True
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='title',
        verbose_name='Жанр',
    )
    description = models.TextField('Описание', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

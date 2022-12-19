# Generated by Django 2.2.16 on 2022-08-24 20:49

from django.db import migrations, models
from django.core.validators import MinValueValidator, MaxValueValidator

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст отзыва')),
                ('score', models.PositiveSmallIntegerField(validators=[MinValueValidator(1, 'Оценка не можыт юыть ниже 1'), MaxValueValidator(10, 'Оценка не должна превышать 10')], verbose_name='Оценка')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
        ),
    ]
    
# Generated by Django 2.2.16 on 2022-08-26 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0002_auto_20220826_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='titles',
            name='genres',
        ),
        migrations.AddField(
            model_name='titles',
            name='genres',
            field=models.ManyToManyField(related_name='title', to='titles.Genres', verbose_name='Жанр'),
        ),
    ]

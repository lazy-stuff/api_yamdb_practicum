# Generated by Django 2.2.16 on 2022-08-29 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0004_auto_20220828_1735'),
    ]

    operations = [
        migrations.RenameField(
            model_name='titles',
            old_name='genres',
            new_name='genre',
        ),
    ]

# Generated by Django 2.2.16 on 2022-08-29 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('titles', '0006_auto_20220829_1247'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='genres',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ['-id']},
        ),
    ]

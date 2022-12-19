import csv

from django.core.management.base import BaseCommand
from rest_framework.generics import get_object_or_404

from reviews.models import Review, Comment
from titles.models import Titles, Categories, Genres
from users.models import CustomUser


def checking_relations(row):
    if 'author' in row:
        row['author'] = get_object_or_404(CustomUser, id=row['author'])
    if 'category' in row:
        row['category'] = get_object_or_404(Categories, id=row['category'])
    return row


class Command(BaseCommand):
    MODELS_DICT = {
        Categories: 'category.csv',
        Genres: 'genre.csv',
        CustomUser: 'users.csv',
        Titles: 'titles.csv',
        Review: 'review.csv',
        Comment: 'comments.csv'
    }

    def handle(self, *args, **options):
        for model in self.MODELS_DICT:
            csvfile = open(f'static/data/{self.MODELS_DICT[model]}',
                           encoding='utf-8')
            reader = csv.DictReader(csvfile)
            for row in reader:
                row = checking_relations(row)
                obj = model(**row)
                obj.save()

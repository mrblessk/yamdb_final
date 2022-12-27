import csv
import os

from django.core.management import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

CSV = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    GenreTitle: 'genre_title.csv',
}


class Command(BaseCommand):
    def _fill_db(self, model, file):
        path = os.path.join('static/data/', file)
        with open(path, 'r', encoding='utf-8') as csv_file:
            file_reader = csv.DictReader(csv_file, delimiter=',')
            for data in file_reader:
                print(f'Заполнены {data} из {file}')
                model.objects.get_or_create(**data)
            print(f'Заполнены модели {model.__name__} из {file}')

    def handle(self, *args, **kwargs):
        for model, file in CSV.items():
            self._fill_db(model, file)

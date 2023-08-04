import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import (Title,
                            User,
                            Category,
                            Comment,
                            GenreTitle,
                            Genre,
                            Review)


class Command(BaseCommand):
    help = 'Импортирует данные в БД из папки static/data'

    def handle(self, *args, **kwargs):
        Title.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()
        Comment.objects.all().delete()
        GenreTitle.objects.all().delete()
        Genre.objects.all().delete()
        Review.objects.all().delete()

        with open(
            './api_yamdb/static/data/category.csv',
            'r',
            newline='',
            encoding='utf8'
        ) as f:
            reader = csv.reader(f)
            headers = next(reader)
            # print('Headers: ', headers)
            for row in reader:
                create = Category.objects.get_or_create(
                    pk=row[0],
                    name=row[1],
                    slug=row[2]
                )
                # print(create)

        with open(
            './api_yamdb/static/data/genre.csv',
            'r',
            newline='',
            encoding='utf8'
        ) as f:
            reader = csv.reader(f)
            headers = next(reader)
            # print('Headers: ', headers)
            for row in reader:
                create = Genre.objects.get_or_create(
                    pk=row[0],
                    name=row[1],
                    slug=row[2]
                )
                # print(create)

        with open(
            './api_yamdb/static/data/titles.csv',
            'r',
            newline='',
            encoding='utf8'
        ) as f:
            reader = csv.reader(f)
            headers = next(reader)
            # print('Headers: ', headers)
            for row in reader:
                create = Title.objects.get_or_create(
                    pk=row[0],
                    name=row[1],
                    year=row[2],
                    category=Category.objects.get(pk=row[3])
                )
                # print(create)

        with open(
            './api_yamdb/static/data/genre_title.csv',
            'r',
            newline='',
            encoding='utf8'
        ) as f:
            reader = csv.reader(f)
            headers = next(reader)
            # print('Headers: ', headers)
            for row in reader:
                create = GenreTitle.objects.get_or_create(
                    pk=row[0],
                    title=Title.objects.get(pk=row[1]),
                    genre=Genre.objects.get(pk=row[2])
                )
                # print(create)

        with open(
            './api_yamdb/static/data/users.csv',
            'r',
            newline='',
            encoding='utf8'
        ) as f:
            reader = csv.reader(f)
            headers = next(reader)
            # print('Headers: ', headers)
            for row in reader:
                create = User.objects.get_or_create(
                    pk=row[0],
                    role=row[3],
                    email=row[2],
                    username=row[1],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[5]
                )
                # print(create)

        with open(
            './api_yamdb/static/data/review.csv',
            'r',
            newline='',
            encoding='utf8'
        ) as f:
            reader = csv.reader(f)
            headers = next(reader)
            # print('Headers: ', headers)
            for row in reader:
                create = Review.objects.get_or_create(
                    pk=row[0],
                    title=Title.objects.get(pk=row[1]),
                    text=row[2],
                    author=User.objects.get(pk=row[3]),
                    score=row[4],
                    pub_date=row[5]
                )
                # print(create)

        with open(
            './api_yamdb/static/data/comments.csv',
            'r',
            newline='',
            encoding='utf8'
        ) as f:
            reader = csv.reader(f)
            headers = next(reader)
            # print('Headers: ', headers)
            for row in reader:
                create = Comment.objects.get_or_create(
                    pk=row[0],
                    review=Review.objects.get(pk=row[1]),
                    text=row[2],
                    author=User.objects.get(pk=row[3]),
                    pub_date=row[4]
                )
                # print(create)

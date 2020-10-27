import csv

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from category.models import Category


class Command(BaseCommand):
    help = "Imports a list of categories form a csv file."

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, 'r') as file:
            if not file.name.endswith('.csv'):
                raise Exception('Unexpected file format. Try it with a valid csv file.')

            reader = csv.reader(file, delimiter='\n')
            reader = list(reader)
            for category_name in reader[1:]:
                try:
                    new_category = Category(name=category_name[0])
                    new_category.save()
                except IntegrityError:
                    print(f'The category "{category_name[0]}" is likely already in the database. Skipping.')

        print('Finished!')

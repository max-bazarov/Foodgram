from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os

from recipes.models import Ingredient

import json

DATA_PATH = os.path.join(settings.BASE_DIR, 'data')


class Command(BaseCommand):
    help = 'loads json to db'

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str)

    def handle(self, *args, **options):
        filepath = os.path.join(DATA_PATH, options['file_name'])
        with open(filepath, 'r') as file:
            data = json.load(file)
            for ingredient in data:
                Ingredient.objects.create(
                    name=ingredient['name'],
                    measurement_unit=ingredient['measurement_unit']
                )

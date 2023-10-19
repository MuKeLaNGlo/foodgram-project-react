import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = "Импорт данных из csv в модель Ingredient"

    def add_arguments(self, parser):
        parser.add_argument("--path", type=str, help="Путь к файлу")

    def handle(self, *args, **options):
        file_path = "data/ingredients.csv"
        with open(file_path, "r") as csv_file:
            reader = csv.reader(csv_file)

            for row in reader:
                try:
                    obj, created = Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1],
                    )
                except Exception as error:
                    print(f"Ошибка в строке {row}: {error}")

        print("Заполнение БД ингридиентами завершено.")

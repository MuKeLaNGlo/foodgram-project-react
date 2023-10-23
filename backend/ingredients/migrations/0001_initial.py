# Generated by Django 4.2.6 on 2023-10-22 19:29

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Ingredient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название ингредиента",
                        max_length=200,
                        verbose_name="Название ингредиента",
                    ),
                ),
                (
                    "measurement_unit",
                    models.CharField(
                        help_text="Введите единицу измерения ингредиента",
                        max_length=10,
                        verbose_name="Единица измерения",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ингредиент",
                "verbose_name_plural": "Ингредиенты",
            },
        ),
    ]
# Generated by Django 4.2.6 on 2023-10-22 19:29

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                        help_text="Введите название тега",
                        max_length=200,
                        verbose_name="Название тега",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        help_text="Цвет тега", max_length=7, verbose_name="Цвет тега"
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Уникальный идентификатор тега",
                        max_length=30,
                        unique=True,
                        verbose_name="Идентификатор тега",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
            },
        ),
    ]

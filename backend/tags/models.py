from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        help_text='Введите название тега',
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет тега',
        help_text='Цвет тега',
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
        verbose_name='Идентификатор тега',
        help_text='Уникальный идентификатор тега',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

from django.core.management.base import BaseCommand

from tags.models import Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        Tag.objects.get_or_create(
            name='Завтрак',
            slug='breakfast',
            color='orange'
        )
        Tag.objects.get_or_create(
            name='Обед',
            slug='lunch',
            color='green'
        )
        Tag.objects.get_or_create(
            name='Ужин',
            slug='dinner',
            color='purple'
        )

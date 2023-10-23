import django_filters
from django_filters.rest_framework import ModelMultipleChoiceFilter

from recipes.models import Favorite, Recipe, ShoppingCart
from tags.models import Tag


class RecipeFilter(django_filters.FilterSet):
    is_favorited = django_filters.NumberFilter(
        method='get_is_favorited',
        label='Избранное',
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='get_is_in_shopping_cart',
        label='В списке покупок',
    )
    author = django_filters.NumberFilter(
        method='filter_by_author',
        label='Автор',
    )
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
        label='Теги',
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'is_favorited', 'is_in_shopping_cart', 'author']

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            favorite_recipes = Favorite.objects.filter(user=user).values_list(
                'recipe__id', flat=True
            )
            queryset = queryset.filter(id__in=favorite_recipes)
        else:
            queryset = queryset.exclude(
                id__in=Favorite.objects.filter(user=user).values_list(
                    'recipe__id', flat=True
                )
            )
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            shopping_cart_recipes = ShoppingCart.objects.filter(
                user=user
            ).values_list(
                'recipe__id', flat=True
            )
            queryset = queryset.filter(id__in=shopping_cart_recipes)
        else:
            queryset = queryset.exclude(
                id__in=ShoppingCart.objects.filter(user=user).values_list(
                    'recipe__id', flat=True
                )
            )
        return queryset

    def filter_by_author(self, queryset, name, value):
        return queryset.filter(author__id=value)

    def filter_tags(self, queryset, name, value):
        tags = value.split(',')
        tag_objects = Tag.objects.filter(name__in=tags)
        return queryset.filter(tags__in=tag_objects)

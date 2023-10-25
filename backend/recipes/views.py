import csv

from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView

from .filters import RecipeFilter
from .mixins import RecipeActionMixin
from .models import Recipe, RecipeIngredient, ShoppingCart
from .pagination import CustomPageNumberPagination
from .serializers import (FavoriteSerializer, RecipeCreateSerializer,
                          RecipeSerializer, ShoppingCartSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipeCreateSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request, pk=None):
        user = request.user

        shopping_cart_recipes = ShoppingCart.objects.filter(
            user=user
        ).values_list(
            'recipe__id', flat=True
        )

        ingredients = (
            RecipeIngredient.objects.filter(recipe__in=shopping_cart_recipes)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(total_amount=Sum('amount'))
        )

        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopping_cart.csv"'

        writer = csv.writer(response)

        writer.writerow(['Ингредиент', 'Количество', 'Единица измерения'])

        writer.writerows(
            [
                [
                    ingredient['ingredient__name'],
                    ingredient['total_amount'],
                    ingredient['ingredient__measurement_unit'],
                ]
                for ingredient in ingredients
            ]
        )

        return response


class FavoriteView(RecipeActionMixin, APIView):
    serializer_class = FavoriteSerializer

    def post(self, request, pk: int):
        error_message = (
            f'Ошибка добавления в избранное. '
            f'Рецепт "{pk}" уже есть в избранном'
        )
        return self.perform_recipe_action(
            request, pk, self.add_to_favorites, error_message
        )

    def delete(self, request, pk: int):
        error_message = (
            f'Ошибка удаление из избранного. '
            f'Рецепт "{pk}" нету в избранном'
        )
        return self.perform_recipe_action(
            request, pk, self.remove_from_favorites, error_message
        )


class ShoppingCartView(RecipeActionMixin, APIView):
    serializer_class = ShoppingCartSerializer

    def post(self, request, pk: int):
        error_message = (
            f'Ошибка добавления в список покупок. '
            f'Рецепт "{pk}" уже есть в списке покупок'
        )
        return self.perform_recipe_action(
            request, pk, self.add_to_shopping_cart, error_message
        )

    def delete(self, request, pk: int):
        error_message = (
            f'Ошибка удаления из списка покупок. '
            f'Рецепт "{pk}" нет в списке покупок'
        )
        return self.perform_recipe_action(
            request, pk, self.remove_from_shopping_cart, error_message
        )

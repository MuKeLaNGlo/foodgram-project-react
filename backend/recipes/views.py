import csv

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import authentication, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RecipeFilter
from .models import Favorite, Recipe, RecipeIngredient, ShoppingCart
from .pagination import CustomPageNumberPagination
from .serializers import (
    FavoriteSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    ShoppingCartSerializer,
)


class RecipeActionMixin(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def perform_recipe_action(
            self, request, pk: int, action_fn, error_message):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if not action_fn(user, recipe):
            return Response(
                {'error': error_message.format(pk)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


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

    def add_to_favorites(self, user, recipe):
        if Favorite.objects.filter(
            user=user, recipe=recipe
        ).exists():
            return False
        Favorite.objects.create(user=user, recipe=recipe)
        return True

    def remove_from_favorites(self, user, recipe):
        if not Favorite.objects.filter(
            user=user, recipe=recipe
        ).exists():
            return False
        Favorite.objects.filter(user=user, recipe=recipe).delete()
        return True


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

    def add_to_shopping_cart(self, user, recipe):
        if ShoppingCart.objects.filter(
            user=user, recipe=recipe
        ).exists():
            return False
        ShoppingCart.objects.create(user=user, recipe=recipe)
        return True

    def remove_from_shopping_cart(self, user, recipe):
        if not ShoppingCart.objects.filter(
            user=user, recipe=recipe
        ).exists():
            return False
        ShoppingCart.objects.filter(
            user=user, recipe=recipe
        ).delete()
        return True

import csv

from django.db.models import Sum
from django.http import HttpResponse
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
            .annotate(amount=Sum('amount'))
        )

        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopping_cart.csv"'

        writer = csv.writer(response)

        writer.writerow(['Ингредиент', 'Количество', 'Единица измерения'])

        for ingredient in ingredients:
            writer.writerow(
                [
                    ingredient['ingredient__name'],
                    ingredient['amount'],
                    ingredient['ingredient__measurement_unit'],
                ]
            )

        return response


class FavoriteView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavoriteSerializer

    def post(self, request, pk: int):
        author = request.user
        if Favorite.objects.filter(user=author, recipe_id=pk).exists():
            return Response(
                {
                    'error': (
                        f'Ошибка добавления в избранное. '
                        f'Рецепт "{id}" уже есть в избранном'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe = Recipe.objects.get(id=pk)
        favorite = Favorite.objects.create(user=author, recipe=recipe)
        serializer = FavoriteSerializer(favorite, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk: int):
        author = request.user
        if not Favorite.objects.filter(user=author, recipe_id=pk).exists():
            return Response(
                {
                    'error': (
                        f'Ошибка удаление из избранного. '
                        f'Рецептa "{id}" нету в избранном'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        Favorite.objects.filter(user=author, recipe_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ShoppingCartSerializer
    pagination_class = CustomPageNumberPagination

    def post(self, request, pk: int):
        user = request.user
        id = pk

        if ShoppingCart.objects.filter(user=user, recipe__id=id).exists():
            return Response(
                {
                    'error': (
                        f'Ошибка добавления в список покупок. '
                        f'Рецепт "{id}" уже есть в списке покупок'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        recipe = Recipe.objects.get(pk=id)
        shopping_cart = ShoppingCart.objects.create(user=user, recipe=recipe)
        serializer = ShoppingCartSerializer(
            shopping_cart,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk: int):
        user = request.user
        recipe_id = pk

        if not ShoppingCart.objects.filter(
            user=user, recipe__id=recipe_id
        ).exists():
            return Response(
                {
                    'error': (
                        f'Ошибка удаления из списка покупок. '
                        f'Рецепта "{recipe_id}" нет в списке покупок'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        ShoppingCart.objects.filter(user=user, recipe_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

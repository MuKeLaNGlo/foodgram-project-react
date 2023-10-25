from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Recipe
from .pagination import CustomPageNumberPagination


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

    @staticmethod
    def add_to_list(user, recipe, model_class):
        if model_class.objects.filter(
            user=user, recipe=recipe
        ).exists():
            return False
        model_class.objects.create(user=user, recipe=recipe)
        return True

    @staticmethod
    def remove_from_list(user, recipe, model_class):
        if not model_class.objects.filter(
            user=user, recipe=recipe
        ).exists():
            return False
        model_class.objects.filter(user=user, recipe=recipe).delete()
        return True

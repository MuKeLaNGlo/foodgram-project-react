from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ingredients.models import Ingredient
from ingredients.serializers import IngredientSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        name = self.request.query_params.get('name', '')
        return Ingredient.objects.filter(name__icontains=name)

    @action(detail=False, methods=['get'])
    def search(self, request):
        name = self.request.query_params.get('name', '')
        ingredients = Ingredient.objects.filter(name__icontains=name)
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

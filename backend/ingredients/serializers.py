from rest_framework import serializers

from .models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.CharField()

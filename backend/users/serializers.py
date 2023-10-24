from django.contrib.auth import get_user_model
from djoser.serializers import TokenCreateSerializer, UserCreateSerializer
from rest_framework import serializers

from recipes.models import Recipe

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('Email не может быть пустым.')
        return value

    def validate_first_name(self, value):
        if not value:
            raise serializers.ValidationError('Имя не может быть пустым.')
        return value

    def validate_last_name(self, value):
        if not value:
            raise serializers.ValidationError('Фамилия не может быть пустой.')
        return value

    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'password')


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'password', 'first_name', 'last_name')


class RecipeInSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username',
                  'first_name', 'last_name', 'recipes']

    def get_recipes(self, user):
        subscribed_author_ids = user.subscriber.values_list(
            'author__id', flat=True
        )
        recipes = Recipe.objects.filter(author_id__in=subscribed_author_ids)
        serializer = RecipeInSubscriptionSerializer(recipes, many=True)
        return serializer.data

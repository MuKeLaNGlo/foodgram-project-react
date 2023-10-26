from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from recipes.models import Recipe
from .models import Subscription

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, author=obj).exists()
        return False

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
                  'first_name', 'last_name', 'is_subscribed')


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
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username',
                  'first_name', 'last_name', 'recipes', 'recipes_count']

    def get_recipes(self, user):
        recipes_limit = self.context.get('recipes_limit')
        subscribed_author_ids = user.subscriber.values_list(
            'author__id', flat=True
        )
        recipes = Recipe.objects.filter(
            author_id__in=subscribed_author_ids
        )[:recipes_limit]
        serializer = RecipeInSubscriptionSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, user):
        subscribed_author_ids = user.subscriber.values_list(
            'author__id', flat=True
        )
        recipes_count = Recipe.objects.filter(
            author_id__in=subscribed_author_ids
        ).count()
        return recipes_count

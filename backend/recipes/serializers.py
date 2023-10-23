from django.core.validators import MinValueValidator
from django.db.models import ImageField
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from ingredients.models import Ingredient
from recipes.models import Favorite, Recipe, RecipeIngredient, ShoppingCart
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer


class CreateRecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient'
    )
    amount = serializers.IntegerField(
        validators=(
            MinValueValidator(
                1, message='Количество ингредиента должно быть 1 или более.'
            ),
        )
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True, required=True, source='recipe_ingredients'
    )
    image = ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_ingredients(self, obj):
        return RecipeIngredientSerializer(
            RecipeIngredient.objects.filter(recipe=obj), many=True
        ).data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(user=user, recipe=obj).exists()
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = CreateRecipeIngredientSerializer(
        many=True, required=True, source='recipe_ingredients'
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(user=user, recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(user=user, recipe=obj).exists()
        return False

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipe_ingredients')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            amount = ingredient['amount']

            RecipeIngredient.objects.create(
                recipe=recipe, ingredient=ingredient['ingredient'],
                amount=amount
            )

        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.image = validated_data.get('image', instance.image)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )

        tags = validated_data.get('tags')
        if tags is not None:
            instance.tags.set(tags)

        ingredients_data = validated_data.get('ingredients')
        if ingredients_data is not None:
            instance.ingredients.clear()

            for ingredient_data in ingredients_data:
                amount = ingredient_data['amount']
                ingredient = get_object_or_404(
                    Ingredient,
                    pk=ingredient_data['id']
                )

                RecipeIngredient.objects.create(
                    recipe=instance, ingredient=ingredient, amount=amount
                )

        instance.save()
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.SerializerMethodField()
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = Favorite
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = fields

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.recipe.image.url
        return request.build_absolute_uri(image_url)


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.SerializerMethodField()
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        model = ShoppingCart
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = fields

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.recipe.image.url
        return request.build_absolute_uri(image_url)

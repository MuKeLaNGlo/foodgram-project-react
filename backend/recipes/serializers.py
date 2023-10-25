from django.core.validators import MinValueValidator
from django.db.models import ImageField
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


class BaseRecipeSerializer(serializers.ModelSerializer):
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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


class RecipeSerializer(BaseRecipeSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientSerializer(
        many=True, required=True, source='recipe_ingredients'
    )
    image = ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeCreateSerializer(BaseRecipeSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = CreateRecipeIngredientSerializer(
        many=True, required=True, source='recipe_ingredients'
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def validate_ingredients(self, value):
        seen_ingredients = set()
        for ingredient in value:
            ingredient_id = ingredient['ingredient'].id
            if ingredient_id in seen_ingredients:
                raise serializers.ValidationError(
                    'Ингредиенты не должны повторяться в рецепте.'
                )
            seen_ingredients.add(ingredient_id)
        return value

    def create_ingredients(self, recipe, ingredients):
        recipe_ingredients = [
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['ingredient'],
                amount=ingredient['amount']
            )
            for ingredient in ingredients
        ]
        RecipeIngredient.objects.bulk_create(recipe_ingredients)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipe_ingredients')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        self.create_ingredients(recipe, ingredients)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.get('tags')
        if tags is not None:
            instance.tags.set(tags)

        ingredients_data = validated_data.get('ingredients')
        if ingredients_data is not None:
            instance.ingredients.clear()
            self.create_ingredients(instance, ingredients_data)

        super().update(instance, validated_data)

        return instance


class BaseRecipeItemSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='recipe.id')
    name = serializers.ReadOnlyField(source='recipe.name')
    image = serializers.SerializerMethodField()
    cooking_time = serializers.ReadOnlyField(source='recipe.cooking_time')

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = fields

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.recipe.image.url
        return request.build_absolute_uri(image_url)


class FavoriteSerializer(BaseRecipeItemSerializer):
    class Meta(BaseRecipeItemSerializer.Meta):
        model = Favorite


class ShoppingCartSerializer(BaseRecipeItemSerializer):
    class Meta(BaseRecipeItemSerializer.Meta):
        model = ShoppingCart

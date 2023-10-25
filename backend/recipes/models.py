from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Автор данного рецепта',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Описание приготовления рецепта',
    )
    ingredients = models.ManyToManyField(
        'ingredients.Ingredient',
        related_name='recipes',
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
        help_text='Выберите ингредиенты для рецепта',
    )
    tags = models.ManyToManyField(
        'tags.Tag',
        related_name='recipes',
        verbose_name='Теги',
        help_text='Выберите теги для рецепта',
    )
    image = models.ImageField(
        upload_to='recipes_images/',
        verbose_name='Изображение рецепта',
        help_text='Загрузите изображение для рецепта',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)',
        help_text='Укажите время приготовления в минутах',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients',
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.PROTECT, verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)], verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} --> ингредиент {self.ingredient}'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Теги рецепта'
        verbose_name_plural = 'Теги рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'],
                name='unique_recipe_tag'
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} --> тег {self.tag}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Пользователь, которому принадлежит корзина',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепты в корзине',
        help_text='Рецепты, добавленные в корзину',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_cart'
            )
        ]

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
        help_text='Пользователь, которому принадлежит понравившийся рецепт',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Рецепт, который понравился пользователю',
    )

    class Meta:
        verbose_name = 'Понравившийся рецепт'
        verbose_name_plural = 'Понравившиеся рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.name}'

from django.contrib import admin
from django.db.models import Count
from django.utils.html import mark_safe

from .models import Favorite, Recipe


class RecipeIngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeTagsInLine(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'text',
        'created_at',
        'author',
        'get_image',
        'count_favorites',
    )
    search_fields = ('name', 'author')
    inlines = (RecipeIngredientsInLine, RecipeTagsInLine)

    def get_image(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" width="80" height="30" />'
        )

    get_image.short_description = 'Изображение'

    def count_favorites(self, obj):
        return obj.favorite_count

    count_favorites.short_description = 'В избранном'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(favorite_count=Count('favorites'))
        return queryset


@admin.register(Favorite)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')

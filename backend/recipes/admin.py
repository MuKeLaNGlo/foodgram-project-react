from django.contrib import admin
from django.utils.html import mark_safe

from .models import Ingredient, Recipe, Tag


class RecipeIngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeTagsInLine(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "text", "pub_date",
        "author", "get_image", "count_favorites"
    )
    search_fields = ("name", "author")
    inlines = (RecipeIngredientsInLine, RecipeTagsInLine)

    def get_image(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" width="80" height="30" />'
        )

    get_image.short_description = "Изображение"

    def count_favorites(self, obj):
        return obj.in_favorite.count()

    count_favorites.short_description = "В избранном"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "measurement_unit")
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "color", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

from django.contrib import admin

from .models import Ingredient, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'image', 'cooking_time')
    list_filter = ('title', 'author', 'description', 'image', 'cooking_time')
    search_fields = ('title', 'author', 'description', 'image', 'cooking_time')
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    list_filter = ('name', 'slug', 'color')
    search_fields = ('name', 'slug', 'color')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'unit')
    list_filter = ('name', 'amount', 'unit')
    search_fields = ('name', 'amount', 'unit')
    empty_value_display = '-пусто-'

from recipes.models import Ingredient, Recipe, Tag
from rest_framework.serializers import ModelSerializer


class RecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'

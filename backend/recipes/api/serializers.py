from rest_framework.serializers import ModelSerializer

from recipes.models import Recipe, Tag, Ingredient


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

from rest_framework.viewsets import ModelViewSet

from recipes.models import Ingredient, Recipe, Tag

from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

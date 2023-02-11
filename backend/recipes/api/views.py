from rest_framework.viewsets import ModelViewSet

from recipes.models import Recipe, Tag, Ingredient
from .serializers import RecipeSerializer, TagSerializer, IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

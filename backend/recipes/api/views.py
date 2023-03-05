from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from core.api.pagination import LimitPageNumberPagination
from core.api.permissions import AuthorOrReadOnly
from core.api.serializers import ListsRecipeSerializer
from lists.models import Cart, Favorite
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag

from .filters import RecipeFilter
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeSerializer, TagSerializer)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination
    permission_classes = (AuthorOrReadOnly,)
    filterset_class = RecipeFilter

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateSerializer(*args, **kwargs)
        return RecipeSerializer(*args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def _add_object(self, model, user, id):
        if model.objects.filter(user=user, recipe__id=id).exists():
            return Response(
                {'errors': 'Рецепт уже добавлен в список'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe = get_object_or_404(Recipe, id=id)
        model.objects.create(user=user, recipe=recipe)
        serializer = ListsRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _delete_object(self, model, user, id):
        obj = model.objects.filter(user=user, recipe__id=id)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт уже удален'}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return self._add_object(Favorite, request.user, pk)
        elif request.method == 'DELETE':
            return self._delete_object(Favorite, request.user, pk)
        return None

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return self._add_object(Cart, request.user, pk)
        elif request.method == 'DELETE':
            return self._delete_object(Cart, request.user, pk)
        return None

    def _prepare_list(self, ingredients):
        ingredients_list = ''
        for ingredient in ingredients:
            ingredients_list += (
                f"{ingredient['ingredient__name']} "
                f"{ingredient['amount']} "
                f"{ingredient['ingredient__measurement_unit']}"
            )
        file = 'food_list.txt'
        response = HttpResponse(ingredients_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file}.txt"'
        return response

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        ingredients = (
            RecipeIngredient.objects.filter(recipe__cart__user=request.user.id)
            .order_by('ingredient__name')
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
        )
        return self._prepare_list(ingredients)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAuthenticatedOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        name = self.request.query_params.get('name')
        queryset = self.queryset

        return queryset.filter(name__istartswith=name)

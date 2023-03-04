from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from core.api.serializers import ListsRecipeSerializer
from core.validators import validate_username
from users.models import Follow, User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if (
            not request.user.is_anonymous
            and Follow.objects.filter(
                author=obj, subscriber=request.user
            ).exists()
        ):
            return True
        return False

    def validate_username(self, username):
        return validate_username(username)


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'id',
            'password',
        )


class FollowSerializer(CustomUserSerializer):
    recipes = ListsRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = ('__all__',)

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()

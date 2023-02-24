from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

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

    def get_is_subscribed(self, obj):
        if Follow.objects.filter(
            follower=obj, followed=self.context['request'].user
        ).exists():
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

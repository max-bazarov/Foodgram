from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.api.pagination import LimitPageNumberPagination
from core.api.permissions import AuthorOrReadOnly
from users.models import Follow

from .serializers import CustomUserSerializer, FollowSerializer

User = get_user_model()


class UserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = LimitPageNumberPagination
    permission_classes = (AuthorOrReadOnly,)

    @action(
        methods=['post'], detail=True, permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        subscriber = request.user
        author = get_object_or_404(User, id=id)

        if subscriber == author:
            return Response(
                {'errors': 'Нельзя подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if Follow.objects.filter(
            subscriber=subscriber, author=author
        ).exists():
            return Response(
                {'errors': 'Вы уже подписаны на данного пользователя'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Follow.objects.create(subscriber=subscriber, author=author)
        serializer = FollowSerializer(author, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        subscriber = request.user
        author = get_object_or_404(User, id=id)
        if subscriber == author:
            return Response(
                {'errors': 'Вы не можете отписываться от самого себя'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        follow = Follow.objects.filter(subscriber=subscriber, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            {'errors': 'Вы уже отписались'}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribers__subscriber=request.user.id)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

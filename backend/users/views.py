from django.contrib.auth import get_user_model
from djoser.views import UserViewSet as DjosrUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from recipes.pagination import CustomPageNumberPagination
from users.models import Subscription
from users.serializers import CustomUserSerializer, SubscriptionSerializer

User = get_user_model()


class UserViewSet(DjosrUserViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPageNumberPagination

    @action(
        detail=False,
        methods=('get',),
        serializer_class=SubscriptionSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        user = self.request.user
        user_subscriptions = Subscription.objects.filter(user=user)
        authors = user_subscriptions.values_list('author__id', flat=True)
        queryset = User.objects.filter(pk__in=authors)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        serializer_class=SubscriptionSerializer
    )
    def subscribe(self, request, id=None):
        target_user = self.get_object()
        current_user = self.request.user

        if target_user == current_user:
            return Response(
                {'errors': 'Нельзя подписаться на самого себя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.method == 'POST':
            if Subscription.objects.filter(
                user=current_user, author=target_user
            ).exists():
                return Response(
                    {'detail': 'Подписка уже оформлена.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            Subscription.objects.create(user=current_user, author=target_user)
            serializer = CustomUserSerializer(target_user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            subscription = Subscription.objects.filter(
                user=current_user, author=target_user
            ).first()

            if subscription:
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(
                {'detail': 'Подписки не существует.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

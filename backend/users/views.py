from django.contrib.auth import get_user_model
from djoser.views import TokenCreateView, UserViewSet
from rest_framework import exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from recipes.pagination import CustomPageNumberPagination
from users.models import Subscription
from users.serializers import CustomUserSerializer, SubscriptionSerializer

User = get_user_model()


class CustomTokenCreateView(TokenCreateView):
    def perform_create(self, serializer):
        token = super().perform_create(serializer)
        user = serializer.validated_data['user']
        return Response(
            {
                'auth_token': token.key,
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            status=status.HTTP_201_CREATED,
        )


class UserViewSet(UserViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPageNumberPagination
    token_create_view = CustomTokenCreateView.as_view()

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=('get',),
        serializer_class=SubscriptionSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        user = self.request.user
        user_subscriptions = Subscription.objects.filter(user=user)
        authors = [item.author.id for item in user_subscriptions]
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

        if current_user.is_anonymous:
            return Response(
                {'detail': 'Учетные данные не были предоставлены.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if target_user == current_user:
            return Response(
                {'errors': 'Нельзя подписаться на самого себя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.method == 'POST':
            if Subscription.objects.filter(
                user=current_user, author=target_user
            ).exists():
                raise exceptions.ValidationError('Подписка уже оформлена.')

            Subscription.objects.create(user=current_user, author=target_user)
            serializer = CustomUserSerializer(target_user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            subscription = Subscription.objects.filter(
                user=current_user, author=target_user
            ).first()

            if subscription:
                subscription.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

            raise exceptions.ValidationError('Подписки не существует.')

        return Response(
            {'detail': 'Метод не разрешен.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

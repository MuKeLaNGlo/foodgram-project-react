from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FavoriteView, RecipeViewSet, ShoppingCartView

app_name = 'recipes'

router_v1 = DefaultRouter()

router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'recipes/<int:pk>/favorite/', FavoriteView.as_view(),
        name='favorite-view'
    ),
    path(
        'recipes/<int:pk>/shopping_cart/',
        ShoppingCartView.as_view(),
        name='shopping-cart-view',
    ),
]

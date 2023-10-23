from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ingredients.views import IngredientViewSet
from recipes.views import FavoriteView, RecipeViewSet, ShoppingCartView
from tags.views import TagViewSet
from users.views import UserViewSet

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router_v1.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
    path(
        'api/recipes/<int:pk>/favorite/', FavoriteView.as_view(),
        name='favorite-view'
    ),
    path(
        'api/recipes/<int:pk>/shopping_cart/',
        ShoppingCartView.as_view(),
        name='shopping-cart-view',
    ),
    path(
        'api/ingredients/',
        IngredientViewSet.as_view({'get': 'list'}),
        name='ingredients-list',
    ),
]

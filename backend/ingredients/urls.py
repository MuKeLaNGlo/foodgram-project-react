from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet

app_name = 'ingredients'

router_v1 = DefaultRouter()

router_v1.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router_v1.urls)),
    path(
        'ingredients/',
        IngredientViewSet.as_view({'get': 'list'}),
        name='ingredients-list',
    ),
]

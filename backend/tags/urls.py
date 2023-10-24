from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet

app_name = 'tags'

router_v1 = DefaultRouter()

router_v1.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router_v1.urls)),
]

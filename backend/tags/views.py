from rest_framework import status, viewsets
from rest_framework.response import Response

from tags.models import Tag
from tags.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

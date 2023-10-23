from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from tags.models import Tag
from tags.serializers import TagSerializer


class TagViewSet(viewsets.ViewSet):
    queryset = Tag.objects.all()

    def retrieve(self, request, pk=None):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tag.DoesNotExist:
            return Response(
                {'detail': 'Страница не найдена.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def list(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post', 'put', 'delete'])
    def not_allowed(self, request):
        return Response(
            {'detail': 'Метод не разрешен.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

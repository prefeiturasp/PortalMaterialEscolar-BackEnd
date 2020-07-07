from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ...models import Material
from ..serializers.material_serializer import (MaterialLookUpSerializer,
                                               MaterialSerializer)


class MateriaisViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id'
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [AllowAny]
    filter_backends = (SearchFilter, OrderingFilter)
    ordering_fields = ('nome',)
    search_fields = ('uuid', 'id', 'nome')

    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        return MaterialSerializer

    @action(detail=False)
    def lookup(self, _):
        return Response(MaterialLookUpSerializer(self.queryset.order_by('nome'), many=True).data)

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny

from ...models import Kit
from ..serializers.kit_serializer import (KitSerializer)


class KitsViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "uuid"
    queryset = Kit.objects.all()
    serializer_class = KitSerializer
    permission_classes = [AllowAny]
    filter_backends = (SearchFilter, OrderingFilter)
    ordering_fields = ('nome',)
    search_fields = ('uuid', 'id', 'nome')

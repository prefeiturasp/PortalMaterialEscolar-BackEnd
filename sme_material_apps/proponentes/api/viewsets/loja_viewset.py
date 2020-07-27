from django.db.models.expressions import RawSQL
from rest_framework.response import Response
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from sme_material_apps.core.models import Kit
from ..serializers.loja_serializer import LojaUpdateFachadaSerializer
from ..serializers.proponente_serializer import LojaCredenciadaSerializer
from ...models.loja import Loja
from ...models.proponente import Proponente
from ...services import haversine


class LojaUpdateFachadaViewSet(mixins.UpdateModelMixin, GenericViewSet):
    lookup_field = "uuid"
    queryset = Loja.objects.all()
    serializer_class = LojaUpdateFachadaSerializer
    permission_classes = [AllowAny]


class LojaViewSet(mixins.ListModelMixin, GenericViewSet):
    lookup_field = "uuid"
    queryset = Loja.objects.all()
    serializer_class = LojaCredenciadaSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Loja.objects.filter(
            proponente__status=Proponente.STATUS_CREDENCIADO,
            latitude__isnull=False,
            longitude__isnull=False
        )
        return queryset

    @action(detail=False, methods=['post'], url_path='lojas')
    def lojas(self, request):
        latitude = self.request.query_params.get('latitude', None)
        longitude = self.request.query_params.get('longitude', None)
        queryset = self.get_queryset()
        if request.data.get('tipo_busca', None) == 'kits':
            kit = Kit.objects.get(uuid=request.data.get('kit'))
            materiais = [m.material.nome for m in kit.materiais_do_kit.all()]
            for material in materiais:
                queryset = queryset.filter(
                    proponente__ofertas_de_materiais__material__nome=material
                )
        elif request.data.get('tipo_busca', None) == 'itens':
            queryset = queryset.filter(
                proponente__ofertas_de_materiais__material__nome__in=request.data.get('materiais')).distinct()

        return Response(
            LojaCredenciadaSerializer(
                queryset,
                context={'latitude': latitude, 'longitude': longitude, 'request': request},
                many=True).data,
            status=status.HTTP_200_OK)

from django.db.models.expressions import RawSQL
from rest_framework.response import Response
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

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
            if request.data.get('kit') == 'EMEI':
                queryset = queryset.filter(
                    proponente__ofertas_de_materiais__material__nome='Agenda Educação Infantil').filter(
                    proponente__ofertas_de_materiais__material__nome='Apontador').filter(
                    proponente__ofertas_de_materiais__material__nome='Borracha').filter(
                    proponente__ofertas_de_materiais__material__nome='Caderno desenho 96 Fls.').filter(
                    proponente__ofertas_de_materiais__material__nome='Caneta hidrográfica (12 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Cola branca').filter(
                    proponente__ofertas_de_materiais__material__nome='Giz de cera grosso Educação Infantil (12 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Lápis de cor (12 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Lápis grafite').filter(
                    proponente__ofertas_de_materiais__material__nome='Massa para modelar (06 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Tesoura').filter(
                    proponente__ofertas_de_materiais__material__nome='Tinta guache (06 cores)')

            elif request.data.get('kit') == 'CICLO_ALFABETIZACAO':
                queryset = queryset.filter(
                    proponente__ofertas_de_materiais__material__nome='Agenda Educação Infantil').filter(
                    proponente__ofertas_de_materiais__material__nome='Apontador').filter(
                    proponente__ofertas_de_materiais__material__nome='Borracha').filter(
                    proponente__ofertas_de_materiais__material__nome='Caderno brochurão 80 Fls.').filter(
                    proponente__ofertas_de_materiais__material__nome='Caderno desenho 96 Fls.').filter(
                    proponente__ofertas_de_materiais__material__nome='Caneta hidrográfica (12 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Cola branca').filter(
                    proponente__ofertas_de_materiais__material__nome='Estojo escolar').filter(
                    proponente__ofertas_de_materiais__material__nome='Giz de cera Ensino Fundamental (12 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Lápis de cor (12 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Lápis grafite').filter(
                    proponente__ofertas_de_materiais__material__nome='Tesoura').filter(
                    proponente__ofertas_de_materiais__material__nome='Régua')

            elif request.data.get('kit') == 'CICLO_INTERDISCIPLINAR':
                queryset = queryset.filter(
                    proponente__ofertas_de_materiais__material__nome='Agenda Educação Infantil').filter(
                    proponente__ofertas_de_materiais__material__nome='Apontador').filter(
                    proponente__ofertas_de_materiais__material__nome='Borracha').filter(
                    proponente__ofertas_de_materiais__material__nome='Caderno universitário 96 Fls.').filter(
                    proponente__ofertas_de_materiais__material__nome='Caderno desenho 96 Fls.').filter(
                    proponente__ofertas_de_materiais__material__nome='Caneta hidrográfica (12 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Cola branca').filter(
                    proponente__ofertas_de_materiais__material__nome='Estojo escolar').filter(
                    proponente__ofertas_de_materiais__material__nome='Giz de cera Ensino Fundamental (12 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Lápis de cor (12 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Lápis grafite').filter(
                    proponente__ofertas_de_materiais__material__nome='Tesoura').filter(
                    proponente__ofertas_de_materiais__material__nome='Régua').filter(
                    proponente__ofertas_de_materiais__material__nome='Caneta esferográfica azul').filter(
                    proponente__ofertas_de_materiais__material__nome='Caneta esferográfica preta')

            elif request.data.get('kit') == 'CICLO_ALTORAL':
                queryset = queryset.filter(
                    proponente__ofertas_de_materiais__material__nome='Apontador').filter(
                    proponente__ofertas_de_materiais__material__nome='Borracha').filter(
                    proponente__ofertas_de_materiais__material__nome='Caderno universitário 200 Fls.').filter(
                    proponente__ofertas_de_materiais__material__nome='Caderno desenho 96 Fls.').filter(
                    proponente__ofertas_de_materiais__material__nome='Caneta hidrográfica (12 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Cola branca').filter(
                    proponente__ofertas_de_materiais__material__nome='Lápis de cor (12 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Lápis grafite').filter(
                    proponente__ofertas_de_materiais__material__nome='Tesoura').filter(
                    proponente__ofertas_de_materiais__material__nome='Régua').filter(
                    proponente__ofertas_de_materiais__material__nome='Caneta esferográfica azul').filter(
                    proponente__ofertas_de_materiais__material__nome='Caneta esferográfica preta').filter(
                    proponente__ofertas_de_materiais__material__nome='Caneta esferográfica vermelha').filter(
                    proponente__ofertas_de_materiais__material__nome='Esquadro 45º').filter(
                    proponente__ofertas_de_materiais__material__nome='Esquadro 60º').filter(
                    proponente__ofertas_de_materiais__material__nome='Transferidor 180º')

            elif request.data.get('kit') == 'MEDIO_EJA_MOVA':
                queryset = queryset.filter(
                    proponente__ofertas_de_materiais__material__nome='Apontador').filter(
                    proponente__ofertas_de_materiais__material__nome='Borracha').filter(
                    proponente__ofertas_de_materiais__material__nome='Caderno universitário 200 Fls.').filter(
                    proponente__ofertas_de_materiais__material__nome='Caderno desenho 96 Fls.').filter(
                    proponente__ofertas_de_materiais__material__nome='Caneta hidrográfica (12 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Cola branca').filter(
                    proponente__ofertas_de_materiais__material__nome='Lápis de cor (12 cores)').filter(
                    proponente__ofertas_de_materiais__material__nome='Lápis grafite').filter(
                    proponente__ofertas_de_materiais__material__nome='Tesoura').filter(
                    proponente__ofertas_de_materiais__material__nome='Régua').filter(
                    proponente__ofertas_de_materiais__material__nome='Caneta esferográfica azul').filter(
                    proponente__ofertas_de_materiais__material__nome='Caneta esferográfica preta').filter(
                    proponente__ofertas_de_materiais__material__nome='Caneta esferográfica vermelha')

        elif request.data.get('tipo_busca', None) == 'itens':
            queryset = queryset.filter(
                proponente__ofertas_de_materiais__material__nome__in=request.data.get('materiais')).distinct()

        return Response(
            LojaCredenciadaSerializer(
                queryset,
                context={'latitude': latitude, 'longitude': longitude, 'request': request},
                many=True).data,
            status=status.HTTP_200_OK)

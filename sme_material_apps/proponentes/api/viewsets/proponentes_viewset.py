from django_filters import rest_framework as filters
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from sme_material_apps.core.models import Material
from ..serializers.proponente_serializer import ProponenteSerializer, ProponenteCreateSerializer

from ...models import Proponente, OfertaDeMaterial


class ProponentesViewSet(mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    permission_classes = [AllowAny]
    lookup_field = 'uuid'
    queryset = Proponente.objects.all()
    serializer_class = ProponenteSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('end_uf',)
    ordering_fields = ('razao_social',)
    search_fields = ('uuid', 'cnpj')

    def get_queryset(self):
        return self.queryset

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return ProponenteSerializer
        else:
            return ProponenteCreateSerializer

    @action(detail=True, methods=['patch'], url_path='tabela-precos')
    def tabela_precos(self, request, uuid):
        proponente = self.get_object()
        for unidade_preco in request.data.get('ofertas_de_materiais'):
            proponente.ofertas_de_materiais.all().delete()
            material = Material.objects.get(nome=unidade_preco.get('nome'))
            oferta_de_material = OfertaDeMaterial(
                proponente=proponente,
                material=material,
                preco=unidade_preco.get('valor')
            )
            oferta_de_material.save()
        return Response(self.get_serializer(proponente).data, status=status.HTTP_200_OK)

    @action(detail=False, url_path='verifica-cnpj')
    def verifica_cnpj(self, request):
        cnpj = request.query_params.get('cnpj')
        if cnpj:
            result = {
                'result': 'OK',
                'cnpj_valido': 'Sim' if Proponente.cnpj_valido(cnpj) else 'Não',
                'cnpj_cadastrado': 'Sim' if Proponente.cnpj_ja_cadastrado(cnpj) else 'Não',

            }
        else:
            result = {
                'result': 'Erro',
                'mensagem': 'Informe o cnpj na url. Ex: /proponentes/verifica-cnpj/?cnpj=53.894.798/0001-29'
            }

        return Response(result)

    @action(detail=True, url_path='concluir-cadastro', methods=['patch'])
    def concluir_cadastro(self, request, uuid):
        try:
            proponente = Proponente.concluir_cadastro(uuid)
        except Exception as e:
            return Response({"detail": e.__str__()}, status.HTTP_400_BAD_REQUEST)
        serializer = ProponenteSerializer(proponente, many=False, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, url_path='verifica-email')
    def verifica_email(self, request):
        email = request.query_params.get('email')
        if email:
            result = {
                'result': 'OK',
                'email_valido': 'Sim' if Proponente.email_valido(email) else 'Não',
                'email_cadastrado': 'Sim' if Proponente.email_ja_cadastrado(email) else 'Não'

            }
        else:
            result = {
                'result': 'Erro',
                'mensagem': 'Informe o email na url. Ex: /proponentes/verifica-email/?email=teste@teste.com'
            }

        return Response(result)

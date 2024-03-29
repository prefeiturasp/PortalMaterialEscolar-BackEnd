import base64
import logging

from django.core.files.base import ContentFile
from django_filters import rest_framework as filters
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from sme_material_apps.core.models import Material, Kit
from ..serializers.loja_serializer import LojaCreateSerializer
from ..serializers.proponente_serializer import ProponenteSerializer, ProponenteCreateSerializer

from ...models import Proponente, OfertaDeMaterial, Loja
from ...services import atualiza_coordenadas_lojas
from ....utils.base64ToFile import base64ToFile

log = logging.getLogger(__name__)


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
        proponente.ofertas_de_materiais.all().delete()

        if not request.data.get('ofertas_de_materiais'):
            msgError = "Pelo menos uma oferta deve ser enviada!"
            log.info(msgError)
            raise ValidationError(msgError)

        for unidade_preco in request.data.get('ofertas_de_materiais'):
            material = Material.objects.get(nome=unidade_preco.get('nome'))
            oferta_de_material = OfertaDeMaterial(
                proponente=proponente,
                material=material,
                preco=unidade_preco.get('valor')
            )
            oferta_de_material.save()

        for kit in proponente.kits.all():
            proponente.kits.remove(kit)

        for kit in request.data.get('kits'):
            kit_obj = Kit.objects.get(uuid=kit)
            proponente.kits.add(kit_obj)

        if proponente.status == Proponente.STATUS_CREDENCIADO:
            proponente.status = Proponente.STATUS_ALTERADO
            proponente.save()

        return Response(ProponenteSerializer(proponente).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='atualiza-lojas')
    def atualiza_lojas(self, request, uuid):
        proponente = self.get_object()
        lojas = request.data.pop('lojas')
        if not lojas:
            msgError = "Pelo menos uma loja precisa ser enviada!"
            log.info(msgError)
            raise ValidationError(msgError)
        lojas_ids = []
        for loja in lojas:
            if loja.get('id', ''):
                lojas_ids.append(loja.get('id'))
                loja_obj = Loja.objects.get(id=loja.get('id', ''))
                loja_obj.numero = loja.get('numero')
                loja_obj.bairro = loja.get('bairro')
                loja_obj.cidade = loja.get('cidade')
                loja_obj.complemento = loja.get('complemento')
                loja_obj.logradouro = loja.get('logradouro')
                loja_obj.uf = loja.get('uf')
                loja_obj.nome_fantasia = loja.get('nome_fantasia')
                loja_obj.telefone = loja.get('telefone')
                loja_obj.site = loja.get('site')

                if loja.get('comprovante_end') is not None:
                    file = base64ToFile(loja.get('comprovante_end'))
                    loja_obj.comprovante_end.save('comprovante_endereco_loja.' + file['ext'], file['data'])
                loja_obj.save()
            else:
                atributos_extras = ['proponente', 'uuid', 'id', 'email', 'criado_em',
                                    'alterado_em', 'latitude', 'longitude', 'cidade',
                                    'uf', 'firstName']
                for attr in atributos_extras:
                    loja.pop(attr, '')
                comprovante = loja.pop('comprovante_end', '')
                loja_object = LojaCreateSerializer().create(loja)
                file = base64ToFile(comprovante)
                loja_object.comprovante_end.save('comprovante_endereco_loja.' + file['ext'], file['data'])
                proponente.lojas.add(loja_object)
                lojas_ids.append(loja_object.id)
        atualiza_coordenadas_lojas(proponente.lojas)

        for loja in proponente.lojas.all():
            if loja.id not in lojas_ids:
                proponente.lojas.remove(loja)

        if proponente.status == Proponente.STATUS_CREDENCIADO:
            proponente.status = Proponente.STATUS_ALTERADO
        proponente.save()

        return Response(ProponenteSerializer(proponente).data, status=status.HTTP_200_OK)

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

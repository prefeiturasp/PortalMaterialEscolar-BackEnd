import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

# from ....core.models import Material
from ...api.serializers.anexo_serializer import AnexoSerializer
from ...api.serializers.loja_serializer import (LojaCreateSerializer,
                                                LojaSerializer)
from ...api.serializers.oferta_de_material_serializer import (
    OfertaDeMaterialCreateSerializer, OfertaDeMaterialSerializer, OfertaDeMaterialLookupSerializer)
from ...models import Proponente, Loja

log = logging.getLogger(__name__)


class ProponenteSerializer(serializers.ModelSerializer):
    ofertas_de_materiais = OfertaDeMaterialSerializer(many=True)
    lojas = LojaSerializer(many=True)
    arquivos_anexos = serializers.ListField(
        child=AnexoSerializer()
    )

    class Meta:
        model = Proponente
        fields = '__all__'


class ProponenteCreateSerializer(serializers.ModelSerializer):

    ofertas_de_materiais = OfertaDeMaterialCreateSerializer(many=True)
    lojas = LojaCreateSerializer(many=True)

    # @staticmethod
    # def categoria_acima_limite(ofertas_de_materiais):
    #     limites_por_categoria = LimiteCategoria.limites_por_categoria_as_dict()
    #
    #     if not limites_por_categoria:
    #         return None
    #
    #     # Inicializa totais por categoria
    #     total_por_categoria = {categoria: 0 for categoria in limites_por_categoria.keys()}
    #
    #     # Sumariza ofertas por categoria
    #     for oferta in ofertas_de_materiais:
    #         total_por_categoria[oferta['material'].categoria] += (oferta['preco'] * oferta['material'].quantidade)
    #
    #     # Encontra e retorna a primeira categoria que ficou acima do limite ou None se nenhuma ficou acima
    #     categoria_acima_do_limite = None
    #     for categoria in total_por_categoria.keys():
    #         if total_por_categoria[categoria] > limites_por_categoria[categoria]:
    #             categoria_acima_do_limite = {'categoria': categoria, 'limite': limites_por_categoria[categoria]}
    #             break
    #
    #     return categoria_acima_do_limite
    #
    # @staticmethod
    # def categoria_faltando_itens(ofertas_de_materiais):
    #     qtd_itens_por_categoria = Material.qtd_itens_por_categoria_as_dict()
    #
    #     categorias_fornecidas = set()
    #
    #     for oferta in ofertas_de_materiais:
    #         categorias_fornecidas.add(oferta['material'].categoria)
    #         qtd_itens_por_categoria[oferta['material'].categoria] -= 1
    #
    #     categoria_faltando_itens = None
    #     for categoria, quantidade in qtd_itens_por_categoria.items():
    #         # Não é obrigatorio fornecer todas as categorias, mas todos os itens das categorias fornecidas
    #         if quantidade > 0 and categoria in categorias_fornecidas:
    #             categoria_faltando_itens = categoria
    #             break
    #     return categoria_faltando_itens

    def create(self, validated_data):
        ofertas_de_materiais = validated_data.pop('ofertas_de_materiais')
        lojas = validated_data.pop('lojas')

        """
        if not ofertas_de_materiais:
            msgError = "Pelo menos uma oferta deve ser enviada!"
            log.info(msgError)
            raise ValidationError(msgError)
        """

        if not lojas:
            msgError = "Pelo menos uma loja precisa ser enviada!"
            log.info(msgError)
            raise ValidationError(msgError)

        # categoria_acima_limite = self.categoria_acima_limite(ofertas_de_materiais)
        # log.info("Categoria acima do limite: {}".format(categoria_acima_limite))
        # if categoria_acima_limite:
        #     log.info("Categoria acima do limite!")
        #     raise ValidationError(
        #         f'Valor total da categoria {Material.CATEGORIA_NOMES[categoria_acima_limite["categoria"]]} '
        #         f'está acima do limite de R$ {categoria_acima_limite["limite"]:.2f}.')
        #
        # categoria_faltando_itens = self.categoria_faltando_itens(ofertas_de_materiais)
        # log.info("Categoria faltando itens: {}".format(categoria_acima_limite))
        # if categoria_faltando_itens:
        #     log.info("Categoria com itens faltando!")
        #     raise ValidationError(
        #         f'Não foram fornecidos todos os itens da categoria {Material.CATEGORIA_NOMES[categoria_faltando_itens]}'
        #         f'. Não é permitido o fornecimento parcial de uma categoria.')

        proponente = Proponente.objects.create(**validated_data)
        log.info("Criando proponente com uuid: {}".format(proponente.uuid))

        ofertas_lista = []
        for oferta in ofertas_de_materiais:
            oferta_object = OfertaDeMaterialCreateSerializer().create(oferta)
            ofertas_lista.append(oferta_object)
        proponente.ofertas_de_materiais.set(ofertas_lista)
        log.info("Proponente {}, Ofertas de materiais: {}".format(proponente.uuid, ofertas_lista))

        lojas_lista = []
        for loja in lojas:
            loja_object = LojaCreateSerializer().create(loja)
            lojas_lista.append(loja_object)
        proponente.lojas.set(lojas_lista)
        log.info("Proponente {}, lojas: {}".format(proponente.uuid, ofertas_lista))
        log.info("Criação de proponente finalizada!")

        return proponente

    class Meta:
        model = Proponente
        exclude = ('id',)


class ProponenteLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proponente
        fields = ('uuid', 'razao_social')


class ProponenteOfertaMaterialSerializer(serializers.ModelSerializer):
    ofertas_de_materiais = OfertaDeMaterialLookupSerializer(many=True)

    class Meta:
        model = Proponente
        fields = ('ofertas_de_materiais',)


class LojaCredenciadaSerializer(serializers.ModelSerializer):
    proponente = ProponenteOfertaMaterialSerializer(many=False)
    email = serializers.SerializerMethodField()
    distancia = serializers.DecimalField(max_digits=4, decimal_places=1)

    def get_email(self, obj):
        return obj.proponente.email

    class Meta:
        model = Loja
        exclude = ('uuid', 'criado_em', 'alterado_em', 'numero_iptu')

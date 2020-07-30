import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from sme_material_apps.proponentes.services import atualiza_coordenadas_lojas
from ...api.serializers.anexo_serializer import AnexoSerializer
from ...api.serializers.loja_serializer import (LojaCreateSerializer,
                                                LojaSerializer)
from ....core.api.serializers.kit_serializer import KitLookupSerializer
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
    kits = KitLookupSerializer(read_only=True, many=True)

    class Meta:
        model = Proponente
        fields = '__all__'


class ProponenteCreateSerializer(serializers.ModelSerializer):

    ofertas_de_materiais = OfertaDeMaterialCreateSerializer(many=True)
    lojas = LojaCreateSerializer(many=True)

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
        atualiza_coordenadas_lojas(proponente.lojas)
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
    distancia = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.proponente.email

    def get_distancia(self, obj):
        if obj.latitude and obj.longitude:
            lat = self.context.get('latitude')
            lon = self.context.get('longitude')
            return round(obj.get_distancia(lat, lon), 2)
        return None

    class Meta:
        model = Loja
        exclude = ('uuid', 'criado_em', 'alterado_em', 'numero_iptu')

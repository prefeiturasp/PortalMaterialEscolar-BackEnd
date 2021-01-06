import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from sme_material_apps.proponentes.services import atualiza_coordenadas_lojas
from ...api.serializers.anexo_serializer import AnexoSerializer
from ...api.serializers.loja_serializer import (LojaCreateSerializer,
                                                LojaSerializer)
from ....core.api.serializers.kit_serializer import KitLookupSerializer
from ...api.serializers.oferta_de_material_serializer import (
    OfertaDeMaterialSerializer, OfertaDeMaterialLookupSerializer)
from ...models import Proponente, Loja
from ....custom_user.models import User

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
    lojas = LojaCreateSerializer(many=True)

    def create(self, validated_data):
        lojas = validated_data.pop('lojas')

        if not lojas:
            msgError = "Pelo menos uma loja precisa ser enviada!"
            log.info(msgError)
            raise ValidationError(msgError)

        proponente = Proponente.objects.create(**validated_data)
        log.info("Criando proponente com uuid: {}".format(proponente.uuid))

        lojas_lista = []
        for loja in lojas:
            loja_object = LojaCreateSerializer().create(loja)
            lojas_lista.append(loja_object)
        proponente.lojas.set(lojas_lista)
        atualiza_coordenadas_lojas(proponente.lojas)
        log.info("Proponente {}, lojas: {}".format(proponente.uuid, lojas_lista))
        log.info("Criação de proponente finalizada!")
        log.info("Criação de usuário do proponente")
        usuario = User.objects.create_user(
            email=proponente.email,
            password="".join([n for n in proponente.cnpj if n.isdigit()])[:5],
            first_name=proponente.responsavel.split(' ')[0],
            last_name=' '.join(proponente.responsavel.split(' ')[1:])
        )
        proponente.usuario = usuario
        proponente.save()
        log.info("Criação de usuário do proponente finalizada")

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
    responsavel = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.proponente.email

    def get_responsavel(self, obj):
        return obj.proponente.responsavel

    def get_distancia(self, obj):
        if obj.latitude and obj.longitude:
            lat = self.context.get('latitude')
            lon = self.context.get('longitude')
            return round(obj.get_distancia(lat, lon), 2)
        return None

    class Meta:
        model = Loja
        exclude = ('uuid', 'criado_em', 'alterado_em', 'numero_iptu')

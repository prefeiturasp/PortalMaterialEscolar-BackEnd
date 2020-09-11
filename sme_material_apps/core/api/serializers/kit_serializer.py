from rest_framework import serializers

from ...models import Kit
from ..serializers.material_kit_serializer import MaterialKitSerializer


class KitSerializer(serializers.ModelSerializer):
    materiais_do_kit = MaterialKitSerializer(many=True)

    class Meta:
        model = Kit
        fields = ('uuid', 'nome', 'preco_maximo', 'ativo', 'ordem', 'materiais_do_kit')


class KitLookupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kit
        fields = ('uuid', 'nome')

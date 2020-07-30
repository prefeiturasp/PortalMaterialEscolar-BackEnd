from rest_framework import serializers

from ...models import Kit
from ..serializers.material_kit_serializer import MaterialKitSerializer


class KitSerializer(serializers.ModelSerializer):
    materiais_do_kit = MaterialKitSerializer(many=True)

    class Meta:
        model = Kit
        fields = ('uuid', 'nome', 'materiais_do_kit', 'preco_maximo', 'ativo')
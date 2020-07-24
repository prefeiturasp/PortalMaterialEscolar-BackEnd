from rest_framework import serializers

from ...models import Kits
from ..serializers.material_kit_serializer import MaterialKitSerializer


class KitSerializer(serializers.ModelSerializer):
    materiais_do_kit = MaterialKitSerializer(many=True)

    class Meta:
        model = Kits
        fields = ('id', 'nome', 'materiais_do_kit')

from rest_framework import serializers

from ...models import MaterialKit
from ..serializers.material_serializer import MaterialSerializer


class MaterialKitSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()

    class Meta:
        model = MaterialKit
        fields = ('id', 'unidades', 'material')

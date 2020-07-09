from rest_framework import serializers

from ...models import OfertaDeMaterial
from ....core.models.material import Material


class OfertaDeMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfertaDeMaterial
        fields = '__all__'


class OfertaDeMaterialCreateSerializer(serializers.ModelSerializer):
    material = serializers.SlugRelatedField(
        slug_field='id',
        required=False,
        queryset=Material.objects.all()
    )

    class Meta:
        model = OfertaDeMaterial
        exclude = ('id', 'proponente')


class OfertaDeMaterialLookupSerializer(serializers.ModelSerializer):
    item = serializers.SlugRelatedField(
        slug_field='nome',
        required=False,
        queryset=Material.objects.all(),
        source='material'
    )

    class Meta:
        model = OfertaDeMaterial
        fields = ('item', 'preco')

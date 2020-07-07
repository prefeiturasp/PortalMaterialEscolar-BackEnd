from rest_framework import serializers

from ...models import Material


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = ('id', 'nome', 'preco_maximo')


class MaterialLookUpSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField('get_nome')

    def get_nome(self, obj):
        return obj.__str__()

    class Meta:
        model = Material
        fields = ('id', 'nome')

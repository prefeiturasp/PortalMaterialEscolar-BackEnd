from rest_framework import fields, serializers

from ...models import Material


class MaterialSerializer(serializers.ModelSerializer):
    categoria = fields.MultipleChoiceField(choices=Material.CATEGORIA_CHOICES)

    class Meta:
        model = Material
        fields = ('id', 'nome', 'preco_maximo', 'categoria')


class MaterialLookUpSerializer(serializers.ModelSerializer):
    nome = serializers.SerializerMethodField('get_nome')

    def get_nome(self, obj):
        return obj.__str__()

    class Meta:
        model = Material
        fields = ('id', 'nome')

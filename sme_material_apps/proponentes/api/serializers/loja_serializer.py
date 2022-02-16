import environ
from rest_framework import serializers

from ...models import Loja

env = environ.Env()
SERVER_NAME = f'{env("SERVER_NAME")}'


class LojaSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    comprovante_end = serializers.SerializerMethodField('get_comprovante_end')

    def get_email(self, obj):
        return obj.proponente.email

    def get_comprovante_end(self, obj):
        if bool(obj.comprovante_end):
            return '%s%s' % (SERVER_NAME, obj.comprovante_end.url)
        else:
            return None

    class Meta:
        model = Loja
        fields = '__all__'


class LojaCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loja
        exclude = ('id', 'proponente')


class LojaUpdateFachadaSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    nome_fantasia = serializers.CharField(read_only=True)

    class Meta:
        model = Loja
        fields = ('uuid', 'nome_fantasia', 'foto_fachada',)

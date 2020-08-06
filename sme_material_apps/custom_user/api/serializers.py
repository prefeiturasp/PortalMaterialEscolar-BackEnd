from rest_framework import serializers

from sme_material_apps.custom_user.models import User
from sme_material_apps.proponentes.api.serializers.proponente_serializer import ProponenteSerializer


class UserSerializer(serializers.ModelSerializer):
    proponente = ProponenteSerializer()

    class Meta:
        model = User
        fields = ("email", "first_name", "proponente")

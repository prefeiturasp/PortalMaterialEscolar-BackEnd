import pytest
from rest_framework import status
from rest_framework.test import APIClient

from ...models.loja import Loja

pytestmark = pytest.mark.django_db


def test_update_loja_fachada(payload_update_fachada_loja, loja_fisica):
    foto_fachada_antes = Loja.objects.get(uuid=str(loja_fisica.uuid)).foto_fachada
    client = APIClient()
    response = client.patch(
        "/lojas/{}/".format(loja_fisica.uuid),
        data=payload_update_fachada_loja,
        format="multipart",
    )
    assert Loja.objects.exists()
    assert response.status_code == status.HTTP_200_OK
    assert (
        Loja.objects.get(uuid=str(loja_fisica.uuid)).foto_fachada != foto_fachada_antes
    )

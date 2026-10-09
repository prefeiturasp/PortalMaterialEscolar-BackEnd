import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

ARQUIVO_TXT_CONTEUDO = b"CONTEUDO TESTE TESTE TESTE"


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def arquivo():
    return SimpleUploadedFile("anexo_teste.txt", ARQUIVO_TXT_CONTEUDO)


@pytest.fixture
def fake_user(client, django_user_model):
    password = "teste"
    email = "fake@user.com"
    user = django_user_model.objects.create_user(email=email, password=password)
    client.login(email=email, password=password)
    return user


@pytest.fixture
def authenticated_client(client, django_user_model):
    email = "teste@teste.com"
    password = "@987654321"
    django_user_model.objects.create_user(email=email, password=password)
    client.login(email=email, password=password)
    return client

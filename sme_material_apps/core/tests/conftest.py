import pytest
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def parametros(arquivo):
    from sme_material_apps.core.models import Parametros

    instrucao = SimpleUploadedFile("instrucao_teste.txt", b"CONTEUDO INSTRUCAO TESTE")
    return Parametros.objects.create(edital=arquivo, instrucao_normativa=instrucao)

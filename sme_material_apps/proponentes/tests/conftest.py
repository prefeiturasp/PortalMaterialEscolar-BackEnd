import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker

PNG_1X1 = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


@pytest.fixture
def proponente():
    return baker.make(
        "Proponente",
        cnpj="00.529.476/0001-14",
        razao_social="Loja Teste SA",
        end_logradouro="Rua Teste, 123",
        end_cidade="Sao Paulo",
        end_uf="SP",
        end_cep="01000-000",
        telefone="(11) 99999-9999",
        email="proponente@teste.com",
        responsavel="Fulano de Tal",
    )


@pytest.fixture
def loja_fisica(proponente):
    foto = SimpleUploadedFile("fachada.png", PNG_1X1, content_type="image/png")
    return baker.make(
        "Loja",
        proponente=proponente,
        nome_fantasia="Loja Teste",
        cep="27600-000",
        endereco="Rua Teste",
        bairro="Centro",
        numero="123",
        complemento="loja 1",
        telefone="(11) 4565-9876",
        numero_iptu="123456",
        foto_fachada=foto,
    )


@pytest.fixture
def payload_update_fachada_loja():
    foto = SimpleUploadedFile("fachada_nova.png", PNG_1X1, content_type="image/png")
    return {"foto_fachada": foto}


@pytest.fixture
def tipo_documento():
    return baker.make(
        "TipoDocumento", nome="Certidão Negativa", obrigatorio=True, visivel=True,
    )

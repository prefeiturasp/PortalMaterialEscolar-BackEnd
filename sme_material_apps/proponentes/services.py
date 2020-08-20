import logging

import requests
from django.db.models import Count, Max
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse

from sme_material_apps.proponentes.models import Loja

user_model = get_user_model()
LAYERS = 'address'
BUNDARY = 'whosonfirst:locality:101965533'
API_URL = f'{settings.GEOREF_API_URL}/v1/search'

log = logging.getLogger(__name__)


def cria_usuario_novo_proponente(proponente):
    user_model.cria_usuario(email=proponente.email, nome=proponente.responsavel, senha=proponente.protocolo)


def muda_status_de_proponentes(queryset, novo_status):
    for proponente in queryset.all():
        if proponente.status != novo_status:
            proponente.status = novo_status
            proponente.save()
        if novo_status == "CREDENCIADO":
            atualiza_coordenadas_lojas(proponente.lojas)


def atualiza_coordenadas(queryset):
    for proponente in queryset.all():
        atualiza_coordenadas_lojas(proponente.lojas)


def envia_email_pendencias(queryset):
    for proponente in queryset.all():
        proponente.comunicar_pendencia()


def gera_excel(request, queryset, csv_data):
    numero_maximo_de_lojas = queryset.annotate(
        num_lojas=Count('lojas')).aggregate(
        Max('num_lojas'))['num_lojas__max']
    for i in range(numero_maximo_de_lojas):
        lojas = []
        for proponente in queryset.all():
            try:
                lojas.append(proponente.lojas.all()[i])
            except IndexError:
                lojas.append({})
        nomes_fantasia = [loja.nome_fantasia if isinstance(loja, Loja) else '' for loja in lojas]
        ceps = [loja.cep if isinstance(loja, Loja) else '' for loja in lojas]
        enderecos = [loja.endereco if isinstance(loja, Loja) else '' for loja in lojas]
        bairros = [loja.bairro if isinstance(loja, Loja) else '' for loja in lojas]
        numeros = [loja.numero if isinstance(loja, Loja) else '' for loja in lojas]
        complementos = [loja.complemento if isinstance(loja, Loja) else '' for loja in lojas]
        telefones = [loja.telefone if isinstance(loja, Loja) else '' for loja in lojas]
        fotos_fachada = [
            request.get_host() + loja.foto_fachada.url if isinstance(loja, Loja) and loja.foto_fachada else '' for
            loja in lojas]
        csv_data.append_col(nomes_fantasia, header=f'loja_{i + 1}_nome_fantasia')
        csv_data.append_col(ceps, header=f'loja_{i + 1}_cep')
        csv_data.append_col(enderecos, header=f'loja_{i + 1}_endereco')
        csv_data.append_col(bairros, header=f'loja_{i + 1}_bairro')
        csv_data.append_col(numeros, header=f'loja_{i + 1}_numero')
        csv_data.append_col(complementos, header=f'loja_{i + 1}_complemento')
        csv_data.append_col(telefones, header=f'loja_{i + 1}_telefone')
        csv_data.append_col(fotos_fachada, header=f'loja_{i + 1}_foto_fachada')
    time = now().astimezone().isoformat('T', 'minutes')[:-6]
    filename = f"proponentes_{time}"
    response = HttpResponse(csv_data.export('xls'), content_type="application/ms-excel")
    response['Content-Disposition'] = f'attachment; filename={filename}.xls'
    return response


def atualiza_coordenadas_lojas(lojas):
    log.info("Atualizando coordendas das lojas físicas")
    for loja in lojas.all():
        params = {
            'text': f'{loja.endereco}, {loja.numero}, {loja.bairro}, {loja.cep}',
            'layers': LAYERS,
            'boundary.gid': BUNDARY}
        try:
            log.info(f"Buscando coordenadas: {params}")
            response = requests.get(API_URL, params=params)
            log.info(f"retorno da api: {response.json()}")
            loja.latitude, loja.longitude = busca_latitude_e_longitude(response.json())
            loja.save()
        except Exception as e:
            log.info(f"Erro ao acessar georef.sme API: {e.__str__()}")


def busca_latitude_e_longitude(payload):
    if not payload['features']:
        raise Exception(f"API não retornou dados válidos: {payload}")

    # A georef.sme API retorna longitude e latitude
    # mas o retorno será latitude e longitude
    return payload['features'][0]['geometry']['coordinates'][::-1]


def haversine(lat, lon):
    """
    Formula haversine para buscar as lojas ordenando pela distancia.
    Para limitar os resultados a partir de uma distancia, descomentar a linha do where.
    """
    return f"""
        SELECT id
            FROM ( SELECT
                    id,
                    111.045 * DEGREES(ACOS(COS(RADIANS({lat}))
                    * COS(RADIANS(latitude))
                    * COS(RADIANS(longitude) - RADIANS({lon})) + SIN(RADIANS({lat}))
                    * SIN(RADIANS(latitude)))) AS distance_in_km
                 FROM proponentes_loja) as distancias
--             WHERE distancias.distance_in_km <= 10
            """

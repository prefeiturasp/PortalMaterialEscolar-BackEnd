import datetime
import environ
import logging

from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models import Q
from smtplib import SMTPServerDisconnected

from ..core.helpers.enviar_email import enviar_email_html

env = environ.Env()

log = logging.getLogger(__name__)


# https://docs.celeryproject.org/en/latest/userguide/tasks.html
@shared_task(
    autoretry_for=(SMTPServerDisconnected,),
    retry_backoff=2,
    retry_kwargs={'max_retries': 8},
)
def enviar_email_confirmacao_cadastro(email, contexto):
    return enviar_email_html(
        'Obrigado pelo envio do seu cadastro',
        'email_confirmacao_cadastro',
        contexto,
        email
    )


@shared_task(
    autoretry_for=(SMTPServerDisconnected,),
    retry_backoff=2,
    retry_kwargs={'max_retries': 8},
)
def enviar_email_confirmacao_pre_cadastro(email, contexto):
    log.info(f'Confirmação de pré-cadastro (Protocolo:{contexto["protocolo"]}) enviada para {email}.')
    return enviar_email_html(
        'Pré-cadastro realizado. Finalize seu cadastro!',
        'email_confirmacao_pre_cadastro',
        contexto,
        email
    )


@shared_task(
    autoretry_for=(SMTPServerDisconnected,),
    retry_backoff=2,
    retry_kwargs={'max_retries': 8},
)
def enviar_email_pendencia(email):
    return enviar_email_html(
        'Cadastro Portal do Material Escolar',
        'email_pendencias_proponente',
        None,
        email
    )


@periodic_task(run_every=crontab(hour=16, minute=0))
def enviar_email_documentos_proximos_vencimento():
    from ..proponentes.models import Proponente
    daqui_a_5_dias = datetime.date.today() + datetime.timedelta(days=5)
    proponentes = Proponente.objects.filter(
        anexos__data_validade=daqui_a_5_dias).filter(
        status__in=[Proponente.STATUS_EM_ANALISE, Proponente.STATUS_CREDENCIADO, Proponente.STATUS_APROVADO]
    )
    for proponente in proponentes.all():
        enviar_email_html(
            'Documento(s) próximo(s) do vencimento',
            'email_documentos_proximos_vencimento',
            None,
            proponente.email
        )


@periodic_task(run_every=crontab(hour=17, minute=0))
def alterar_status_documentos_vencidos():
    from ..proponentes.models import Anexo
    anexos = Anexo.objects.filter(data_validade__lt=datetime.date.today()).filter(~Q(status=Anexo.STATUS_VENCIDO))
    anexos.update(status=Anexo.STATUS_VENCIDO)

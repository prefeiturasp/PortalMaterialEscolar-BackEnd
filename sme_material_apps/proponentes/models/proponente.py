import environ
import logging

from brazilnum.cnpj import validate_cnpj
from django.core import validators
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from sme_material_apps.core.helpers.validar_email import email_valido
from sme_material_apps.core.models_abstracts import ModeloBase
from sme_material_apps.core.models import Kit

from ..tasks import (enviar_email_confirmacao_cadastro,
                     enviar_email_confirmacao_pre_cadastro)
from .tipo_documento import TipoDocumento
from .validators import cep_validation, cnpj_validation, phone_validation

log = logging.getLogger(__name__)


class Proponente(ModeloBase):
    historico = AuditlogHistoryField()

    UF_CHOICES = (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MG', 'Minas Gerais'),
        ('MS', 'Mato Grosso do Sul'),
        ('MT', 'Mato Grosso'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('PR', 'Paraná'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('RS', 'Rio Grande do Sul'),
        ('SC', 'Santa Catarina'),
        ('SE', 'Sergipe'),
        ('SP', 'São Paulo'),
        ('TO', 'Tocantins'),
    )

    # Status Choice
    STATUS_INSCRITO = 'INSCRITO'
    STATUS_BLOQUEADO = 'BLOQUEADO'
    STATUS_EM_PROCESSO = 'EM_PROCESSO'
    STATUS_APROVADO = 'APROVADO'
    STATUS_REPROVADO = 'REPROVADO'
    STATUS_PENDENTE = 'PENDENTE'
    STATUS_EM_ANALISE = 'EM_ANALISE'
    STATUS_CREDENCIADO = 'CREDENCIADO'

    STATUS_NOMES = {
        STATUS_INSCRITO: 'Inscrito',
        STATUS_BLOQUEADO: 'Bloqueado',
        STATUS_EM_PROCESSO: 'Pré-cadastro',
        STATUS_APROVADO: 'Aprovado',
        STATUS_REPROVADO: 'Reprovado',
        STATUS_PENDENTE: 'Pendente',
        STATUS_EM_ANALISE: 'Em análise',
        STATUS_CREDENCIADO: 'Credenciado'
    }

    STATUS_CHOICES = (
        (STATUS_INSCRITO, STATUS_NOMES[STATUS_INSCRITO]),
        (STATUS_BLOQUEADO, STATUS_NOMES[STATUS_BLOQUEADO]),
        (STATUS_EM_PROCESSO, STATUS_NOMES[STATUS_EM_PROCESSO]),
        (STATUS_APROVADO, STATUS_NOMES[STATUS_APROVADO]),
        (STATUS_REPROVADO, STATUS_NOMES[STATUS_REPROVADO]),
        (STATUS_PENDENTE, STATUS_NOMES[STATUS_PENDENTE]),
        (STATUS_EM_ANALISE, STATUS_NOMES[STATUS_EM_ANALISE]),
        (STATUS_CREDENCIADO, STATUS_NOMES[STATUS_CREDENCIADO]),
    )

    cnpj = models.CharField(
        "CNPJ", max_length=20, validators=[cnpj_validation], blank=True, null=True, default="", unique=True
    )
    razao_social = models.CharField("Razão Social", max_length=255, blank=True, null=True)

    end_logradouro = models.CharField(
        'endereço',
        max_length=100,
        blank=True
    )

    end_complemento = models.CharField(
        'complemento',
        max_length=100,
        blank=True
    )

    end_numero = models.CharField(
        'número',
        max_length=20,
        blank=True
    )

    end_bairro = models.CharField(
        'bairro',
        max_length=100,
        blank=True
    )

    end_cidade = models.CharField(
        'cidade',
        max_length=80,
        blank=True
    )

    end_uf = models.CharField(
        'estado',
        max_length=2,
        blank=True,
        choices=UF_CHOICES,
        default='SP'
    )

    end_cep = models.CharField(
        'cep',
        max_length=10,
        blank=True,
        default='',
        validators=[cep_validation]
    )

    telefone = models.CharField(
        "Telefone", max_length=20, validators=[phone_validation], blank=True, null=True, default=""
    )

    email = models.CharField(
        "E-mail", max_length=255, validators=[validators.EmailValidator()], blank=True, null=True, default="",
        unique=True
    )

    responsavel = models.CharField("Responsável", max_length=255, blank=True, null=True)

    kits = models.ManyToManyField(Kit, blank=True, related_name='proponentes')

    status = models.CharField(
        'status',
        max_length=15,
        choices=STATUS_CHOICES,
        default=STATUS_EM_PROCESSO
    )

    def __str__(self):
        return f"{self.responsavel} - {self.email} - {self.telefone}"

    def comunicar_pre_cadastro(self):
        if self.email:
            log.info(f'Enviando confirmação de pré-cadastro (Protocolo:{self.protocolo}) enviada para {self.email}.')

            env = environ.Env()
            url = f'https://{env("SERVER_NAME")}/fornecedor/cadastro?uuid={self.uuid}'
            enviar_email_confirmacao_pre_cadastro.delay(self.email,
                                                        {'protocolo': self.protocolo, 'url_cadastro': url})

    def comunicar_cadastro(self):
        if self.email:
            log.info(f'Enviando confirmação de cadastro (Protocolo:{self.protocolo}) enviada para {self.email}.')
            enviar_email_confirmacao_cadastro.delay(self.email, {'protocolo': self.protocolo})

    @property
    def protocolo(self):
        return f'{self.uuid.urn[9:17].upper()}'

    @property
    def arquivos_anexos(self):
        return self.anexos.all()

    @property
    def valor_total_kits(self):
        kits_valores = []
        for kit in self.kits.all():
            valor_kit = 0
            for material_kit in kit.materiais_do_kit.all():
                valor_kit += self.ofertas_de_materiais.get(material=material_kit.material).preco * material_kit.unidades
            kits_valores.append({'kit': kit, 'valor_kit': valor_kit})
        return kits_valores

    @classmethod
    def cnpj_ja_cadastrado(cls, cnpj):
        return cls.objects.filter(cnpj=cnpj).exists()

    @staticmethod
    def cnpj_valido(cnpj):
        return validate_cnpj(cnpj)

    @classmethod
    def bloqueia_por_cnpj(cls, cnpj):
        Proponente.objects.filter(cnpj=cnpj).update(status=Proponente.STATUS_BLOQUEADO)

    @classmethod
    def desbloqueia_por_cnpj(cls, cnpj):
        Proponente.objects.filter(cnpj=cnpj).update(status=Proponente.STATUS_INSCRITO)

    @classmethod
    def documentos_obrigatorios_enviados(cls, proponente):
        """Valida se os documentos obrigatórios foram enviados."""
        tipos_obrigatorios = TipoDocumento.objects.filter(obrigatorio=True, visivel=True)
        anexos_obrigatorios = proponente.anexos.filter(tipo_documento__obrigatorio=True)

        return tipos_obrigatorios.count() == anexos_obrigatorios.count()

    @classmethod
    def concluir_cadastro(cls, uuid):
        proponente = Proponente.objects.get(uuid=uuid)
        if not cls.documentos_obrigatorios_enviados(proponente):
            log.info(f'Erro na conclusão de Cadastro. Faltam documentos obrigatórios. UUID:{uuid}')
            raise Exception("Documento obrigatório ainda precisa ser enviado!")
        proponente.status = Proponente.STATUS_INSCRITO
        proponente.save()
        log.info(f'Cadastro concluído. UUID:{uuid}')
        proponente.comunicar_cadastro()

    @classmethod
    def email_ja_cadastrado(cls, email):
        return cls.objects.filter(email=email).exists()

    @staticmethod
    def email_valido(email):
        return email_valido(email)

    class Meta:
        verbose_name = "Proponente"
        verbose_name_plural = "Proponentes"


@receiver(post_save, sender=Proponente)
def proponente_post_save(instance, created, **kwargs):
    if created and instance:
        instance.comunicar_pre_cadastro()


auditlog.register(Proponente)

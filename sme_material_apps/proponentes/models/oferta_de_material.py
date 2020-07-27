from django.db import models

from sme_material_apps.core.models_abstracts import ModeloBase
from .proponente import Proponente
from ...core.models.material import Material


# from auditlog.models import AuditlogHistoryField
# from auditlog.registry import auditlog


class OfertaDeMaterial(ModeloBase):
    # historico = AuditlogHistoryField()

    proponente = models.ForeignKey(Proponente, on_delete=models.CASCADE, related_name='ofertas_de_materiais',
                                   blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='proponentes')
    preco = models.DecimalField('Preço', max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.material.nome} - {self.preco} - {self.proponente.razao_social if self.proponente else ''}"

    class Meta:
        verbose_name = "oferta de material"
        verbose_name_plural = "ofertas de material"
        unique_together = ['proponente', 'material']
        ordering = ('material',)

# TODO Corrigir erro que da ao excluir um proponente quando o log da oferta de material está ativo
# auditlog.register(OfertaDeMaterial)

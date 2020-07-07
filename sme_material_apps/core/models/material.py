from django.db import models

from sme_material_apps.core.models_abstracts import ModeloBase


class Material(ModeloBase):

    nome = models.CharField('Item de Material', unique=True, max_length=100, blank=True, default='')

    preco_maximo = models.DecimalField('Preço Máximo', max_digits=9, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "Item de Material"
        verbose_name_plural = "Itens de Materiais"

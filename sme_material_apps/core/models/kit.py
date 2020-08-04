from django.db import models

from sme_material_apps.core.models_abstracts import ModeloBase


class Kit(ModeloBase):
    nome = models.CharField('Nome do kit', unique=True, max_length=150)
    preco_maximo = models.DecimalField('Preço Máximo', max_digits=9, decimal_places=2, default=0.00)
    ordem = models.PositiveSmallIntegerField(default=0)
    ativo = models.BooleanField("Está ativo?", default=True)

    def __str__(self):
        return self.nome

    @property
    def qtd_itens(self):
        return self.materiais_do_kit.count()

    class Meta:
        verbose_name = "Kit"
        verbose_name_plural = "Kits"
        ordering = ('ordem',)

from django.db import models

from sme_material_apps.core.models_abstracts import ModeloBase


class Kits(ModeloBase):
    nome = models.CharField('Nome do kit', unique=True, max_length=150)

    def __str__(self):
        return self.nome

    @property
    def qtd_itens(self):
        return self.materiais_do_kit.count()

    class Meta:
        verbose_name = "Kit"
        verbose_name_plural = "Kits"

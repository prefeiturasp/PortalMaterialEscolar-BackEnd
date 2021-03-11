from django.db import models

from sme_material_apps.core.models_abstracts import ModeloBase, SingletonModel


class Parametros(SingletonModel, ModeloBase):
    edital = models.FileField(blank=True, null=True)
    instrucao_normativa = models.FileField('Instrução Normativa', blank=True, null=True)
    especificacoes_itens_kits = models.FileField("Especificações de itens dos kits", blank=True, null=True)

    def __str__(self):
        return self.edital.name

    class Meta:
        verbose_name = "Parâmetro"
        verbose_name_plural = "Parâmetros"

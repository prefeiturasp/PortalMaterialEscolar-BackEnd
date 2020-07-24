from django.db import models

from sme_material_apps.core.models_abstracts import ModeloBase
from ..models.material import Material
from ..models.kit import Kit


class MaterialKit(ModeloBase):
    kit = models.ForeignKey(Kit, on_delete=models.CASCADE, related_name='materiais_do_kit')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='kit_do_material')
    unidades = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.kit.nome} >> ({self.material.nome}: {self.unidades} unidade(s))'

    class Meta:
        verbose_name = "Material do Kit"
        verbose_name_plural = "Materiais dos Kits"

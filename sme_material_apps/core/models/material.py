import logging
from django.db import models
from multiselectfield import MultiSelectField

from sme_material_apps.core.models_abstracts import ModeloBase

log = logging.getLogger(__name__)


class Material(ModeloBase):
    # Categoria Choice
    CATEGORIA_INFANTIL_BERCARIO = 'BERCARIO'
    CATEGORIA_INFANTIL_MINI_GRUPO = 'MINI_GRUPO'
    CATEGORIA_INFANTIL_EMEI = 'EMEI'
    CATEGORIA_FUNDAMENTAL_CICLO_ALFABETIZACAO = 'CICLO_ALFABETIZACAO'
    CATEGORIA_FUNDAMENTAL_CICLO_INTERDISCIPLINAR = 'CICLO_INTERDISCIPLINAR'
    CATEGORIA_FUNDAMENTAL_CICLO_ALTORAL = 'CICLO_ALTORAL'
    CATEGORIA_MEDIO_EJA_MOVA = 'MEDIO_EJA_MOVA'

    CATEGORIA_NOMES = {
        CATEGORIA_INFANTIL_BERCARIO: 'Kit Infantil (Berçário I e II)',
        CATEGORIA_INFANTIL_MINI_GRUPO: 'Kit Infantil (Mini grupo I e II)',
        CATEGORIA_INFANTIL_EMEI: 'Kit Infantil (EMEI - Infantil I e II)',
        CATEGORIA_FUNDAMENTAL_CICLO_ALFABETIZACAO: 'Kit Ensino Fundamental - Ciclo alfabetização (1º ao 3º ano)',
        CATEGORIA_FUNDAMENTAL_CICLO_INTERDISCIPLINAR: 'Kit Ensino Fundamental - Ciclo interdisciplinar (4º ao 6º ano)',
        CATEGORIA_FUNDAMENTAL_CICLO_ALTORAL: 'Kit Ensino Fundamental - Ciclo Autoral (7º ao 9º ano)',
        CATEGORIA_MEDIO_EJA_MOVA: 'Kit Ensino Médio, EJA e MOVA',
    }

    CATEGORIA_CHOICES = (
        (CATEGORIA_INFANTIL_BERCARIO, CATEGORIA_NOMES[CATEGORIA_INFANTIL_BERCARIO]),
        (CATEGORIA_INFANTIL_MINI_GRUPO, CATEGORIA_NOMES[CATEGORIA_INFANTIL_MINI_GRUPO]),
        (CATEGORIA_INFANTIL_EMEI, CATEGORIA_NOMES[CATEGORIA_INFANTIL_EMEI]),
        (CATEGORIA_FUNDAMENTAL_CICLO_ALFABETIZACAO, CATEGORIA_NOMES[CATEGORIA_FUNDAMENTAL_CICLO_ALFABETIZACAO]),
        (CATEGORIA_FUNDAMENTAL_CICLO_INTERDISCIPLINAR, CATEGORIA_NOMES[CATEGORIA_FUNDAMENTAL_CICLO_INTERDISCIPLINAR]),
        (CATEGORIA_FUNDAMENTAL_CICLO_ALTORAL, CATEGORIA_NOMES[CATEGORIA_FUNDAMENTAL_CICLO_ALTORAL]),
        (CATEGORIA_MEDIO_EJA_MOVA, CATEGORIA_NOMES[CATEGORIA_MEDIO_EJA_MOVA]),
    )

    nome = models.CharField('Item de Material', unique=True, max_length=100, blank=True, default='')

    preco_maximo = models.DecimalField('Preço Máximo', max_digits=9, decimal_places=2, default=0.00)

    categoria = MultiSelectField(
        choices=CATEGORIA_CHOICES,
        default=CATEGORIA_FUNDAMENTAL_CICLO_ALFABETIZACAO,
    )

    def __str__(self):

        return f'{self.nome}'

    @classmethod
    def categorias_to_json(cls):
        result = []
        for categoria in cls.CATEGORIA_CHOICES:
            materiais = []
            for material in cls.objects.filter(categoria=categoria[0]):
                materiais.append(
                    {
                        "id": material.id,
                        "nome": material.nome,
                        "quantidade": material.quantidade,
                        "descricao": material.__str__()
                    }
                )
            choice = {
                'id': categoria[0],
                'nome': categoria[1],
                'materiais': materiais
            }
            result.append(choice)
        return result

    class Meta:
        verbose_name = "Item de Material"
        verbose_name_plural = "Itens de Materiais"
        ordering = ('nome',)

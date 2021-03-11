from django.urls import include, path

from rest_framework import routers

# Importe aqui as rotas das demais aplicações
from sme_material_apps.proponentes.urls import router as proponentes_router
from .viewsets.edital_viewset import EditalViewSet
from .viewsets.instrucao_normativa_viewset import InstrucaoNormativaViewSet
from .viewsets.especificacoes_itens_kits import EspecificacoesItensKitsViewSet
from .viewsets.materiais_viewset import MateriaisViewSet
from .viewsets.kits_viewset import KitsViewSet
from .viewsets.version_viewset import ApiVersion

router = routers.DefaultRouter()

router.register('api-version', ApiVersion, basename='Version')
router.register('kits', KitsViewSet)
router.register('materiais', MateriaisViewSet)
router.register('edital', EditalViewSet, basename='Edital')
router.register('instrucao-normativa', InstrucaoNormativaViewSet, basename='InstrucaoNormativa')
router.register('especificacoes-itens', EspecificacoesItensKitsViewSet, basename='EspecificacaoesItens')

# Adicione aqui as rotas das demais aplicações para que as urls sejam exibidas na API Root do DRF
router.registry.extend(proponentes_router.registry)

urlpatterns = [
    path('', include(router.urls))
]

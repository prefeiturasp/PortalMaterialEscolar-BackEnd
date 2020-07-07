from django.urls import include, path

from rest_framework import routers

# Importe aqui as rotas das demais aplicações
from .viewsets.edital_viewset import EditalViewSet
from .viewsets.instrucao_normativa_viewset import InstrucaoNormativaViewSet
from .viewsets.materiais_viewset import MateriaisViewSet
from .viewsets.version_viewset import ApiVersion

router = routers.DefaultRouter()

router.register('api-version', ApiVersion, basename='Version')
router.register('materiais', MateriaisViewSet)
router.register('edital', EditalViewSet, basename='Edital')
router.register('instrucao-normativa', InstrucaoNormativaViewSet, basename='InstrucaoNormativa')

urlpatterns = [
    path('', include(router.urls))
]

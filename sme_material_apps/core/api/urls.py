from django.urls import include, path

from rest_framework import routers

# Importe aqui as rotas das demais aplicações
from .viewsets.version_viewset import ApiVersion

router = routers.DefaultRouter()

router.register('api-version', ApiVersion, basename='Version')

urlpatterns = [
    path('', include(router.urls))
]

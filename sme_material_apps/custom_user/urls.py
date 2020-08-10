from django.urls import include, path
from rest_framework import routers

from .api import viewsets

router = routers.DefaultRouter()

router.register('usuarios', viewsets.UserViewSet, 'Usuários')

urlpatterns = [
    path('', include(router.urls))
]

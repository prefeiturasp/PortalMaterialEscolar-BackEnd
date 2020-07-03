from django.contrib import admin

from .models import Parametros


@admin.register(Parametros)
class ParametrosAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return not Parametros.objects.exists()

    list_display = ('id', 'edital', 'instrucao_normativa', 'alterado_em')
    readyonly_field = ('alterado_em',)
    fields = ('edital', 'instrucao_normativa')

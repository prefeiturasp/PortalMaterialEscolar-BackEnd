from django.contrib import admin

from .models import Parametros, Material, Kit, MaterialKit


class MateriaisFornecidosInLine(admin.TabularInline):
    model = MaterialKit
    extra = 1  # Quantidade de linhas que serão exibidas.


@admin.register(Kit)
class KitAdmin(admin.ModelAdmin):
    @staticmethod
    def qtd_itens(kit):
        return kit.materiais_do_kit.count()

    list_display = ('nome', 'ativo', 'ordem', 'qtd_itens', 'preco_maximo')
    ordering = ('nome',)
    search_fields = ('nome',)
    inlines = [MateriaisFornecidosInLine]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    ordering = ('nome',)
    search_fields = ('nome',)
    fields = ('nome',)


@admin.register(Parametros)
class ParametrosAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return not Parametros.objects.exists()

    list_display = ('id', 'edital', 'instrucao_normativa', 'especificacoes_itens_kits','alterado_em')
    readyonly_field = ('alterado_em',)
    fields = ('edital', 'instrucao_normativa', 'especificacoes_itens_kits', 'email_sme')

from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.admin import SimpleListFilter
from import_export import resources
from import_export.fields import Field
from rangefilter.filter import DateRangeFilter

from .models import (Proponente, OfertaDeMaterial, Loja, Anexo, TipoDocumento)
from .services import muda_status_de_proponentes, atualiza_coordenadas, envia_email_pendencias, gera_excel


class MateriaisFornecidosInLine(admin.TabularInline):
    model = OfertaDeMaterial
    extra = 1  # Quantidade de linhas que serão exibidas.


class LojasInLine(admin.StackedInline):
    model = Loja
    extra = 1  # Quantidade de linhas que serão exibidas.


class AnexosInLine(admin.TabularInline):
    model = Anexo
    extra = 1  # Quantidade de linhas que serão exibidas.


class RequestModelResource(resources.ModelResource):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RequestModelResource, self).__init__(*args, **kwargs)


class ProponenteResource(RequestModelResource):
    status = Field()
    agenda_educacao_infantil = Field()
    agenda_ensino_fundamental = Field()
    apontador = Field()
    borracha = Field()
    caderno_brochurao_80_fls = Field()
    caderno_desenho_96_fls = Field()
    caderno_universitario_200_fls = Field()
    caderno_universitario_96_fls = Field()
    caneta_esferografica_azul = Field()
    caneta_esferografica_preta = Field()
    caneta_esferografica_vermelha = Field()
    caneta_hidrografica_12_cores = Field()
    cola_branca = Field()
    esquadro_45 = Field()
    esquadro_60 = Field()
    estojo_escolar = Field()
    giz_de_cera_ensino_fundamental_12_cores = Field()
    giz_de_cera_grosso_educacao_infantil_12_cores = Field()
    lapis_de_cor_12_cores = Field()
    lapis_grafite = Field()
    massa_para_modelar_06_cores = Field()
    regua = Field()
    tesoura = Field()
    tinta_guache_06_cores = Field()
    transferidor_180 = Field()
    kit_educacao_infantil_emei = Field()
    kit_ensino_fundamental_ciclo_alfabetizacao = Field()
    kit_ensino_fundamental_ciclo_interdisciplinar = Field()
    kit_ensino_fundamental_ciclo_autoral = Field()
    kit_ensino_medio_eja_mova = Field()

    def dehydrate_status(self, obj):
        return obj.get_status_display()

    def dehydrate_agenda_educacao_infantil(self, obj):
        return obj.get_preco_material("Agenda Educação Infantil")

    def dehydrate_agenda_ensino_fundamental(self, obj):
        return obj.get_preco_material("Agenda Ensino Fundamental")

    def dehydrate_apontador(self, obj):
        return obj.get_preco_material("Apontador")

    def dehydrate_borracha(self, obj):
        return obj.get_preco_material("Borracha")

    def dehydrate_caderno_brochurao_80_fls(self, obj):
        return obj.get_preco_material("Caderno brochurão 80 Fls.")

    def dehydrate_caderno_desenho_96_fls(self, obj):
        return obj.get_preco_material("Caderno desenho 96 Fls.")

    def dehydrate_caderno_universitario_200_fls(self, obj):
        return obj.get_preco_material("Caderno universitário 200 Fls.")

    def dehydrate_caderno_universitario_96_fls(self, obj):
        return obj.get_preco_material("Caderno universitário 96 Fls.")

    def dehydrate_caneta_esferografica_azul(self, obj):
        return obj.get_preco_material("Caneta esferográfica azul")

    def dehydrate_caneta_esferografica_preta(self, obj):
        return obj.get_preco_material("Caneta esferográfica preta")

    def dehydrate_caneta_esferografica_vermelha(self, obj):
        return obj.get_preco_material("Caneta esferográfica vermelha")

    def dehydrate_caneta_hidrografica_12_cores(self, obj):
        return obj.get_preco_material("Caneta hidrográfica (12 cores)")

    def dehydrate_cola_branca(self, obj):
        return obj.get_preco_material("Cola branca")

    def dehydrate_esquadro_45(self, obj):
        return obj.get_preco_material("Esquadro 45º")

    def dehydrate_esquadro_60(self, obj):
        return obj.get_preco_material("Esquadro 60º")

    def dehydrate_estojo_escolar(self, obj):
        return obj.get_preco_material("Estojo escolar")

    def dehydrate_giz_de_cera_ensino_fundamental_12_cores(self, obj):
        return obj.get_preco_material("Giz de cera Ensino Fundamental (12 cores)")

    def dehydrate_giz_de_cera_grosso_educacao_infantil_12_cores(self, obj):
        return obj.get_preco_material("Giz de cera grosso Educação Infantil (12 cores)")

    def dehydrate_lapis_de_cor_12_cores(self, obj):
        return obj.get_preco_material("Lápis de cor (12 cores)")

    def dehydrate_lapis_grafite(self, obj):
        return obj.get_preco_material("Lápis grafite")

    def dehydrate_massa_para_modelar_06_cores(self, obj):
        return obj.get_preco_material("Massa para modelar (06 cores)")

    def dehydrate_regua(self, obj):
        return obj.get_preco_material("Régua")

    def dehydrate_tesoura(self, obj):
        return obj.get_preco_material("Tesoura")

    def dehydrate_tinta_guache_06_cores(self, obj):
        return obj.get_preco_material("Tinta guache (06 cores)")

    def dehydrate_transferidor_180(self, obj):
        return obj.get_preco_material("Transferidor 180º")

    def dehydrate_kit_educacao_infantil_emei(self, obj):
        return obj.get_valor_kit("Kit Educação Infantil (Infantil I e II - EMEI)")

    def dehydrate_kit_ensino_fundamental_ciclo_alfabetizacao(self, obj):
        return obj.get_valor_kit("Kit Ensino Fundamental - Ciclo de Alfabetização (1º ao 3º ano)")

    def dehydrate_kit_ensino_fundamental_ciclo_interdisciplinar(self, obj):
        return obj.get_valor_kit("Kit Ensino Fundamental - Ciclo Interdisciplinar (4º ao 6º ano)")

    def dehydrate_kit_ensino_fundamental_ciclo_autoral(self, obj):
        return obj.get_valor_kit("Kit Ensino Fundamental - Ciclo Autoral (7º ao 9º ano)")

    def dehydrate_kit_ensino_medio_eja_mova(self, obj):
        return obj.get_valor_kit("Kit Ensino Médio/EJA e MOVA")

    class Meta:
        model = Proponente
        fields = ('status', 'cnpj', 'razao_social', 'end_cep', 'end_bairro', 'end_logradouro',
                  'end_numero', 'end_complemento', 'end_uf', 'end_uf', 'responsavel', 'telefone',
                  'email')
        export_order = fields


class TemAnexosReprovadosOuVencidosFilter(SimpleListFilter):
    title = 'tem anexos reprovados ou vencidos'
    parameter_name = 'anexos'

    def lookups(self, request, model_admin):
        return [('Reprovados ou Vencidos', 'Reprovados ou Vencidos'),
                ('Reprovados', 'Reprovados'),
                ('Vencidos', 'Vencidos')]

    def queryset(self, request, queryset):
        if self.value() == 'Reprovados ou Vencidos':
            return queryset.filter(anexos__status__in=["REPROVADO", "VENCIDO"]).distinct()
        elif self.value() == 'Reprovados':
            return queryset.filter(anexos__status="REPROVADO").distinct()
        elif self.value() == 'Vencidos':
            return queryset.filter(anexos__status="VENCIDO").distinct()
        else:
            return queryset


@admin.register(Proponente)
class ProponenteAdmin(admin.ModelAdmin):
    resource_class = ProponenteResource

    def get_resource_kwargs(self, request, *args, **kwargs):
        """ Passa o objeto request para **kwargs """
        return {'request': request}

    def muda_status_para_inscrito(self, request, queryset):
        muda_status_de_proponentes(queryset, Proponente.STATUS_INSCRITO)
        self.message_user(request, f'Status alterados para {Proponente.STATUS_NOMES[Proponente.STATUS_INSCRITO]}.')

    muda_status_para_inscrito.short_description = f'Status ==> {Proponente.STATUS_NOMES[Proponente.STATUS_INSCRITO]}.'

    def muda_status_para_em_processo(self, request, queryset):
        muda_status_de_proponentes(queryset, Proponente.STATUS_EM_PROCESSO)
        self.message_user(request, f'Status alterados para {Proponente.STATUS_NOMES[Proponente.STATUS_EM_PROCESSO]}.')

    muda_status_para_em_processo.short_description = \
        f'Status ==> {Proponente.STATUS_NOMES[Proponente.STATUS_EM_PROCESSO]}.'

    def muda_status_para_aprovado(self, request, queryset):
        muda_status_de_proponentes(queryset, Proponente.STATUS_APROVADO)
        self.message_user(request, f'Status alterados para {Proponente.STATUS_NOMES[Proponente.STATUS_APROVADO]}.')

    muda_status_para_aprovado.short_description = f'Status ==> {Proponente.STATUS_NOMES[Proponente.STATUS_APROVADO]}.'

    def muda_status_para_reprovado(self, request, queryset):
        muda_status_de_proponentes(queryset, Proponente.STATUS_REPROVADO)
        self.message_user(request, f'Status alterados para {Proponente.STATUS_NOMES[Proponente.STATUS_REPROVADO]}.')

    muda_status_para_reprovado.short_description = f'Status ==> {Proponente.STATUS_NOMES[Proponente.STATUS_REPROVADO]}.'

    def muda_status_para_pendente(self, request, queryset):
        muda_status_de_proponentes(queryset, Proponente.STATUS_PENDENTE)
        self.message_user(request, f'Status alterados para {Proponente.STATUS_NOMES[Proponente.STATUS_PENDENTE]}.')

    muda_status_para_pendente.short_description = f'Status ==> {Proponente.STATUS_NOMES[Proponente.STATUS_PENDENTE]}.'

    def muda_status_para_em_analise(self, request, queryset):
        muda_status_de_proponentes(queryset, Proponente.STATUS_EM_ANALISE)
        self.message_user(request, f'Status alterados para {Proponente.STATUS_NOMES[Proponente.STATUS_EM_ANALISE]}.')

    muda_status_para_em_analise.short_description = f'Status ==> {Proponente.STATUS_NOMES[Proponente.STATUS_EM_ANALISE]}.'

    def muda_status_para_credenciado(self, request, queryset):
        muda_status_de_proponentes(queryset, Proponente.STATUS_CREDENCIADO)
        self.message_user(request, f'Status alterados para {Proponente.STATUS_NOMES[Proponente.STATUS_CREDENCIADO]}.')

    muda_status_para_credenciado.short_description = f'Status ==> {Proponente.STATUS_NOMES[Proponente.STATUS_CREDENCIADO]}.'

    def atualiza_coordenadas_action(self, request, queryset):
        atualiza_coordenadas(queryset)
        self.message_user(request, f'Coordenadas das lojas físicas para proponentes CREDENCIADOS foram atualizados.')

    atualiza_coordenadas_action.short_description = f'Atualiza coordenadas.'

    def envia_email_pendencias_action(self, request, queryset):
        if len(queryset) != len(queryset.filter(status=Proponente.STATUS_PENDENTE)):
            self.message_user(request, "Selecione apenas proponentes com status pendente", level=messages.ERROR)
        else:
            envia_email_pendencias(queryset)
            self.message_user(request, f'E-mail de pendências enviado com sucesso.')

    envia_email_pendencias_action.short_description = f'Enviar e-mail de pendências'

    def gera_excel_action(self, request, queryset):
        csv_data = ProponenteResource().export(queryset)
        return gera_excel(request, queryset, csv_data)

    gera_excel_action.short_description = f'Gerar excel'

    def gera_excel_action(self, request, queryset):
        csv_data = ProponenteResource().export(queryset)
        return gera_excel(request, queryset, csv_data)

    gera_excel_action.short_description = f'Gerar excel'

    def task_email_documentos_proximos_vencimento_action(self, request, queryset):
        from .tasks import enviar_email_documentos_proximos_vencimento
        enviar_email_documentos_proximos_vencimento()

    task_email_documentos_proximos_vencimento_action.short_description = f'Rodar task email docs prox. venc.'

    def task_alterar_status_documentos_vencidos_action(self, request, queryset):
        from .tasks import alterar_status_documentos_vencidos
        alterar_status_documentos_vencidos()

    task_alterar_status_documentos_vencidos_action.short_description = f'Rodar task alterar docs vencidos'

    def ultima_alteracao(self, obj):
        return obj.alterado_em.strftime("%d/%m/%Y %H:%M:%S")

    ultima_alteracao.admin_order_field = 'alterado_em'
    ultima_alteracao.short_description = 'Última alteração'

    def kits_fornecidos(self, obj):
        lista_kits = '<ul>'
        lista_kits += "\n".join(['<li>{}</li>'.format(str(k)) for k in obj.kits.all()])
        lista_kits += '&nbsp;' * 150 + '</ul>'
        return mark_safe(lista_kits)

    def get_valor_total_kits(self, obj):
        lista_valor = ''
        lista_valor += "\n".join(
            ['{}</br>'.format(f"{k['kit']} - VALOR: {k['valor_kit']}") for k in obj.valor_total_kits])
        return mark_safe(lista_valor)

    get_valor_total_kits.short_description = 'Kits e Valores Fornecidos'

    actions = [
        'verifica_bloqueio_cnpj',
        'muda_status_para_aprovado',
        'muda_status_para_reprovado',
        'muda_status_para_pendente',
        'muda_status_para_em_analise',
        'muda_status_para_inscrito',
        'muda_status_para_em_processo',
        'muda_status_para_credenciado',
        'atualiza_coordenadas_action',
        'envia_email_pendencias_action',
        'gera_excel_action',
        'task_email_documentos_proximos_vencimento_action',
        'task_alterar_status_documentos_vencidos_action']
    list_display = ('protocolo', 'cnpj', 'razao_social', 'responsavel', 'telefone', 'email', 'status',
                    'ultima_alteracao', 'kits_fornecidos')
    ordering = ('-alterado_em',)
    search_fields = ('uuid', 'cnpj', 'razao_social', 'responsavel')
    filter_horizontal = ('kits',)
    list_filter = ('status', ('criado_em', DateRangeFilter), TemAnexosReprovadosOuVencidosFilter)
    inlines = [MateriaisFornecidosInLine, LojasInLine, AnexosInLine]
    readonly_fields = ('uuid', 'id', 'cnpj', 'razao_social', 'get_valor_total_kits')
    exclude = ('kits',)


@admin.register(OfertaDeMaterial)
class OfertaDeMaterialAdmin(admin.ModelAdmin):
    @staticmethod
    def protocolo(oferta):
        return oferta.proponente.protocolo

    list_display = ('protocolo', 'proponente', 'material', 'preco')
    ordering = ('proponente',)
    search_fields = ('proponente__uuid', 'material__nome',)
    list_filter = ('material',)


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    @staticmethod
    def protocolo(loja):
        return loja.proponente.protocolo

    @staticmethod
    @mark_safe
    def fachada(loja):
        foto = loja.foto_fachada
        return f'<img src="{foto.url}" width="64px"/>' if foto else ""

    fachada.allow_tags = True

    def save_model(self, request, obj, form, change):
        if not obj.latitude:
            messages.add_message(request, messages.WARNING, 'Ao cadastrar uma loja nova é necessário atualizar as '
                                                            'coordenadas no cadastro do proponente.')
        super(LojaAdmin, self).save_model(request, obj, form, change)

    list_display = ('protocolo', 'nome_fantasia', 'fachada', 'cep', 'endereco', 'numero', 'complemento', 'bairro',
                    'site')
    ordering = ('nome_fantasia',)
    search_fields = ('proponente__uuid', 'nome_fantasia',)
    list_filter = ('bairro',)


@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    def inverte_visivel(self, request, queryset):
        for tipo_documento in queryset.all():
            tipo_documento.visivel = not tipo_documento.visivel
            tipo_documento.save()

        self.message_user(request, "Parâmetro 'visível' atualizado.")

    inverte_visivel.short_description = "Inverter o parâmetro 'visível' "

    def inverte_obrigatorio(self, request, queryset):
        for tipo_documento in queryset.all():
            tipo_documento.obrigatorio = not tipo_documento.obrigatorio
            tipo_documento.save()

        self.message_user(request, "Parâmetro 'obrigatório' atualizado.")

    inverte_obrigatorio.short_description = "Inverter o parâmetro 'obrigatório' "

    list_display = ('nome', 'obrigatorio', 'visivel', 'tem_data_validade', 'obrigatorio_sme')
    ordering = ('nome',)
    search_fields = ('nome',)
    list_filter = ('obrigatorio', 'visivel')
    actions = ['inverte_visivel', 'inverte_obrigatorio']

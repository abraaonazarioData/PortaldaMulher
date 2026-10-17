from django.contrib import admin
from .admin_extra import admin_extra_urls
from django.urls import path
from .models import BannerInicial, AtividadeDestaque, ParceiroInstitucional, PlanosMetas, VisitCounter, PanelVisitCounter, RedeProtecao, Tema, PrecisoAjuda, MateriaisEducativos, PaineisDados, ServicosPublicos, Legislacao, SobrePortal, Ouvidoria, EstatisticaViolencia

admin.site.site_header = "Administração do Portal Mulher"
admin.site.site_title = "Portal Mulher MT"
admin.site.index_title = "Painel de Controle"

@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'ordem')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome',)
# Base admin for proxy models
class BaseThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'image_tag')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'text')
    readonly_fields = ('image_tag',)
    
    fieldsets = (
        ('Informações Gerais', {
            'fields': ('title', 'slug', 'text')
        }),
        ('Mídia', {
            'fields': ('image', 'image_tag', 'icon')
        }),
        ('Links Externos', {
            'fields': ('link_url', 'youtube_video_url', 'reference_sources')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(tema__slug=self.theme_slug)

    def save_model(self, request, obj, form, change):
        if not obj.tema_id:
            tema, _ = Tema.objects.get_or_create(slug=self.theme_slug)
            obj.tema = tema
        super().save_model(request, obj, form, change)

@admin.register(PrecisoAjuda)
class PrecisoAjudaAdmin(BaseThemeAdmin):
    theme_slug = 'preciso-de-ajuda'

@admin.register(MateriaisEducativos)
class MateriaisEducativosAdmin(BaseThemeAdmin):
    theme_slug = 'materiais-educativos'

@admin.register(PaineisDados)
class PaineisDadosAdmin(BaseThemeAdmin):
    theme_slug = 'paineis-e-dados'

@admin.register(ServicosPublicos)
class ServicosPublicosAdmin(BaseThemeAdmin):
    theme_slug = 'servicos-e-politicas-publicas'

@admin.register(Legislacao)
class LegislacaoAdmin(BaseThemeAdmin):
    theme_slug = 'legislacao'

@admin.register(SobrePortal)
class SobrePortalAdmin(BaseThemeAdmin):
    theme_slug = 'sobre-o-portal'

@admin.register(RedeProtecao)
class RedeProtecaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'cidade', 'telefone')
    list_filter = ('tipo', 'cidade')
    search_fields = ('nome', 'cidade', 'endereco')

@admin.register(EstatisticaViolencia)
class EstatisticaViolenciaAdmin(admin.ModelAdmin):
    list_display = ('municipio', 'tipo_crime', 'ano', 'mes', 'quantidade')
    list_filter = ('ano', 'municipio', 'tipo_crime')
    search_fields = ('municipio', 'tipo_crime')

# @admin.register(VisitCounter)
# class VisitCounterAdmin(admin.ModelAdmin):
#     list_display = ('id', 'count')

# @admin.register(PanelVisitCounter)
# class PanelVisitCounterAdmin(admin.ModelAdmin):
#     list_display = ('id', 'count')
@admin.register(BannerInicial)
class BannerInicialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ordem', 'ativo')
    list_editable = ('ordem', 'ativo')

@admin.register(AtividadeDestaque)
class AtividadeDestaqueAdmin(admin.ModelAdmin):
    change_form_template = 'admin/core/atividadedestaque/change_form.html'
    list_display = ('miniatura', 'titulo', 'chapeu', 'autor', 'status_badge', 'data_publicacao')
    list_display_links = ('miniatura', 'titulo')
    list_filter = ('status', 'chapeu', 'data_publicacao')
    search_fields = ('titulo', 'chapeu', 'linha_fina', 'autor', 'corpo')
    date_hierarchy = 'data_publicacao'
    readonly_fields = ('previa_capa', 'criado_em', 'atualizado_em')
    actions = ['publicar', 'voltar_rascunho']

    # Ordem: Chapéu → Título → Linha fina → Autor → Foto de capa → Crédito → Corpo → Publicar
    fieldsets = (
        ('1. Identificação da matéria', {
            'classes': ('col-principal',),
            'fields': ('chapeu', 'titulo', 'linha_fina', 'autor'),
        }),
        ('3. Corpo da matéria', {
            'classes': ('col-principal',),
            'description': 'Para inserir fotos entre os parágrafos, use o botão de imagem do editor. '
                           'Depois clique na foto e use "Legenda" para escrever a legenda e o crédito '
                           '(ex.: "Reunião com a rede de proteção — Foto: Fulano/Secom-MT").',
            'fields': ('corpo',),
        }),
        ('Publicação', {
            'classes': ('col-lateral',),
            'fields': ('status', 'data_publicacao', 'slug', 'criado_em', 'atualizado_em'),
        }),
        ('2. Foto de capa', {
            'classes': ('col-lateral',),
            'fields': ('imagem', 'previa_capa', 'credito_imagem'),
        }),
    )

    @admin.display(description='Capa')
    def miniatura(self, obj):
        from django.utils.html import format_html
        if obj.imagem:
            return format_html('<img src="{}" style="width:72px;height:48px;object-fit:cover;border-radius:4px;">', obj.imagem.url)
        return '—'

    @admin.display(description='Pré-visualização da capa')
    def previa_capa(self, obj):
        from django.utils.html import format_html
        if obj and obj.imagem:
            return format_html('<img src="{}" style="width:100%;max-width:340px;aspect-ratio:16/9;object-fit:cover;border-radius:6px;">', obj.imagem.url)
        return 'A miniatura aparece após salvar.'

    @admin.display(description='Situação', ordering='status')
    def status_badge(self, obj):
        from django.utils.html import format_html
        from django.utils import timezone
        if obj.status == obj.STATUS_RASCUNHO:
            cor, txt = '#6c757d', 'Rascunho'
        elif obj.data_publicacao > timezone.now():
            cor, txt = '#f0ad4e', 'Agendada'
        else:
            cor, txt = '#28a745', 'Publicada'
        return format_html('<span style="background:{};color:#fff;padding:3px 10px;border-radius:12px;font-size:.8rem;">{}</span>', cor, txt)

    @admin.action(description='Publicar notícias selecionadas')
    def publicar(self, request, queryset):
        queryset.update(status=AtividadeDestaque.STATUS_PUBLICADO)

    @admin.action(description='Voltar para rascunho')
    def voltar_rascunho(self, request, queryset):
        queryset.update(status=AtividadeDestaque.STATUS_RASCUNHO)

    def _redirect_preview(self, obj):
        from django.shortcuts import redirect
        return redirect('noticia_previa', pk=obj.pk)

    def response_add(self, request, obj, post_url_continue=None):
        if '_previa' in request.POST:
            return self._redirect_preview(obj)
        return super().response_add(request, obj, post_url_continue)

    def response_change(self, request, obj):
        if '_previa' in request.POST:
            return self._redirect_preview(obj)
        return super().response_change(request, obj)

@admin.register(ParceiroInstitucional)
class ParceiroInstitucionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem')
    list_editable = ('ordem',)

@admin.register(PlanosMetas)
class PlanosMetasAdmin(BaseThemeAdmin):
    theme_slug = 'planos-e-metas'

# Register Ouvidoria admin using BaseThemeAdmin
@admin.register(Ouvidoria)
class OuvidoriaAdmin(BaseThemeAdmin):
    theme_slug = 'ouvidoria'

# Extend admin URLs to include custom view
_original_get_urls = admin.site.get_urls

def _custom_admin_urls():
    return admin_extra_urls + _original_get_urls()

admin.site.get_urls = _custom_admin_urls

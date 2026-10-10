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
    list_display = ('titulo', 'categoria', 'data_publicacao')
    search_fields = ('titulo', 'categoria')

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

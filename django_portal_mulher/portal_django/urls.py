from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found
from django.views.generic import RedirectView
from core import views, views_dashboard

handler404 = lambda request, exception: page_not_found(request, exception, template_name='404.html')

urlpatterns = [
    path('SysteGEVM9x2/', admin.site.urls),
    path('painel/', views_dashboard.dashboard_home, name='dashboard_home'),
    path('', views.home, name='home'),
    path('servicos', views.servicos, name='servicos'),
    path('legislacao', views.legislacao, name='legislacao'),
    path('atendimentos', views.atendimentos, name='atendimentos'),
    path('ocorrencias', views.ocorrencias, name='ocorrencias'),
    path('acessibilidade', views.acessibilidade, name='acessibilidade'),
    path('planos-metas', views.planos_metas, name='planos_metas'),
    path('estatisticas', views.estatisticas, name='estatisticas'),
    path('noticias', views.atividades, name='atividades'),
    path('atividades', RedirectView.as_view(pattern_name='atividades', permanent=True)),
    path('noticias/previa/<int:pk>/', views.noticia_previa, name='noticia_previa'),
    path('noticias/<slug:slug>/', views.noticia_detalhe, name='noticia_detalhe'),
    path('noticia/<int:id>/', views.noticia_por_id, name='noticia_por_id'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('modulo1', views.modulo1, name='modulo1'),
    path('modulo2', views.modulo2, name='modulo2'),
    path('modulo3', views.modulo3, name='modulo3'),
    path('modulo4', views.modulo4, name='modulo4'),
    path('documentos', views.documentos, name='documentos'),
    path('conheca', views.conheca, name='conheca'),
    path('modulo5', views.modulo5, name='modulo5'),
    path('modulo6', views.modulo6, name='modulo6'),
    path('modulo7', views.modulo7, name='modulo7'),
    path('modulo8', views.modulo8, name='modulo8'),
    path('politica-privacidade', views.politica_privacidade, name='politica_privacidade'),
    path('mapa-site', views.mapa_site, name='mapa_site'),
    path('fonar', views.fonar, name='fonar'),
    path('fale-cidadao', views.fale_cidadao, name='fale_cidadao'),
    path('bi-interativo', views.bi_interativo, name='bi_interativo'),
    path('chat', views.chat_api, name='chat_api'),
]

from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

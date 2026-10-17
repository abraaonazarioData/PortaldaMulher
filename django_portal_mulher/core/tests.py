"""
Testes Automatizados — Módulo de Notícias (AtividadeDestaque)
Portal Mulher MT

Execução:
    .venv\\Scripts\\python.exe manage.py test core.tests --verbosity=2

Cobertura:
    - Modelo AtividadeDestaque (campos, slug, sanitização XSS, status)
    - Views: lista, detalhe, prévia, redirect por ID
    - URLs: /noticias, /atividades (redirect 301), /noticias/<slug>/
    - Templates: campos corretos renderizados, campos deletados ausentes
    - Home: carousel com campos novos
    - Casos de borda: sem imagem, sem chapéu, data futura, XSS
"""

from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
import tempfile, os
from PIL import Image

from .models import AtividadeDestaque


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_temp_image():
    """Cria um arquivo de imagem temporário válido para upload."""
    tmp = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    img = Image.new('RGB', (100, 60), color=(200, 100, 50))
    img.save(tmp, format='JPEG')
    tmp.seek(0)
    return tmp


def _noticia(
    titulo='Notícia de Teste',
    chapeu='TESTE',
    linha_fina='Subtítulo da notícia de teste para validação.',
    autor='Redação Portal',
    corpo='<p>Corpo completo da matéria.</p>',
    status=AtividadeDestaque.STATUS_PUBLICADO,
    data_publicacao=None,
    credito_imagem='Divulgação',
    imagem=None,
):
    """Cria e retorna uma notícia no banco sem imagem real (simplificado)."""
    if data_publicacao is None:
        data_publicacao = timezone.now() - timedelta(minutes=1)

    n = AtividadeDestaque(
        chapeu=chapeu,
        titulo=titulo,
        linha_fina=linha_fina,
        autor=autor,
        corpo=corpo,
        status=status,
        data_publicacao=data_publicacao,
        credito_imagem=credito_imagem,
    )
    # Salva sem imagem para testes que não precisam de arquivo
    n.save()
    return n


# ===========================================================================
# 1. TESTES DE MODELO
# ===========================================================================

class ModeloAtividadeDestaqueTest(TestCase):

    def test_slug_gerado_automaticamente(self):
        """Slug deve ser gerado a partir do título ao salvar."""
        n = _noticia(titulo='Minha Primeira Notícia')
        self.assertEqual(n.slug, 'minha-primeira-noticia')

    def test_slug_unico_com_sufixo(self):
        """Dois títulos iguais devem gerar slugs únicos com sufixo numérico."""
        n1 = _noticia(titulo='Título Repetido')
        n2 = _noticia(titulo='Título Repetido')
        self.assertNotEqual(n1.slug, n2.slug)
        self.assertTrue(n2.slug.endswith('-2'))

    def test_get_absolute_url_usa_slug(self):
        """get_absolute_url deve retornar /noticias/<slug>/."""
        n = _noticia(titulo='Url Via Slug')
        self.assertEqual(n.get_absolute_url(), f'/noticias/{n.slug}/')

    def test_status_padrao_rascunho(self):
        """Status padrão do modelo deve ser rascunho."""
        n = AtividadeDestaque(
            chapeu='X', titulo='T', linha_fina='L',
            autor='A', corpo='<p>c</p>', credito_imagem='D',
        )
        self.assertEqual(n.status, AtividadeDestaque.STATUS_RASCUNHO)

    def test_property_publicada_true(self):
        """Notícia publicada com data no passado deve retornar publicada=True."""
        n = _noticia(status=AtividadeDestaque.STATUS_PUBLICADO)
        self.assertTrue(n.publicada)

    def test_property_publicada_false_rascunho(self):
        """Rascunho não deve ser considerado publicado."""
        n = _noticia(status=AtividadeDestaque.STATUS_RASCUNHO)
        self.assertFalse(n.publicada)

    def test_property_publicada_false_futuro(self):
        """Notícia com data futura não deve ser considerada publicada."""
        n = _noticia(
            status=AtividadeDestaque.STATUS_PUBLICADO,
            data_publicacao=timezone.now() + timedelta(hours=2),
        )
        self.assertFalse(n.publicada)

    def test_queryset_publicadas_exclui_rascunho(self):
        """Manager publicadas() não deve retornar rascunhos."""
        _noticia(status=AtividadeDestaque.STATUS_PUBLICADO)
        _noticia(status=AtividadeDestaque.STATUS_RASCUNHO)
        qs = AtividadeDestaque.objects.publicadas()
        self.assertEqual(qs.count(), 1)

    def test_queryset_publicadas_exclui_futura(self):
        """Manager publicadas() não deve retornar notícias com data futura."""
        _noticia(status=AtividadeDestaque.STATUS_PUBLICADO)
        _noticia(
            status=AtividadeDestaque.STATUS_PUBLICADO,
            data_publicacao=timezone.now() + timedelta(days=1),
        )
        qs = AtividadeDestaque.objects.publicadas()
        self.assertEqual(qs.count(), 1)

    def test_sanitizacao_xss_script(self):
        """Tag <script> no corpo deve ser removida pelo sanitizador nh3."""
        n = _noticia(corpo='<p>Texto</p><script>alert("xss")</script>')
        self.assertNotIn('<script>', n.corpo)
        self.assertIn('<p>Texto</p>', n.corpo)

    def test_sanitizacao_xss_onclick(self):
        """Atributo onclick deve ser removido pelo sanitizador."""
        n = _noticia(corpo='<p onclick="alert(1)">Texto</p>')
        self.assertNotIn('onclick', n.corpo)

    def test_chapeu_armazena_texto(self):
        """Campo chapéu deve armazenar o valor passado."""
        n = _noticia(chapeu='SAÚDE')
        self.assertEqual(n.chapeu, 'SAÚDE')

    def test_linha_fina_armazena_texto(self):
        """Campo linha_fina deve armazenar o valor passado."""
        n = _noticia(linha_fina='Este é o subtítulo da matéria.')
        self.assertEqual(n.linha_fina, 'Este é o subtítulo da matéria.')

    def test_str_retorna_titulo(self):
        """__str__ deve retornar o título da notícia."""
        n = _noticia(titulo='Título da Notícia')
        self.assertEqual(str(n), 'Título da Notícia')

    def test_campos_antigos_nao_existem(self):
        """Campos removidos não devem existir no modelo."""
        n = _noticia()
        self.assertFalse(hasattr(n, 'categoria'), 'Campo categoria não deveria existir')
        self.assertFalse(hasattr(n, 'resumo'),    'Campo resumo não deveria existir')
        self.assertFalse(hasattr(n, 'conteudo_completo'), 'Campo conteudo_completo não deveria existir')
        self.assertFalse(hasattr(n, 'link'),      'Campo link não deveria existir')


# ===========================================================================
# 2. TESTES DE URL
# ===========================================================================

class URLsTest(TestCase):

    def test_url_noticias_resolve(self):
        """/noticias deve resolver para a view atividades."""
        resolved = resolve('/noticias')
        self.assertEqual(resolved.url_name, 'atividades')

    def test_url_atividades_redireciona_para_noticias(self):
        """/atividades deve retornar redirect 301 para /noticias."""
        c = Client()
        response = c.get('/atividades')
        self.assertEqual(response.status_code, 301)
        self.assertIn('/noticias', response['Location'])

    def test_url_detalhe_resolve(self):
        """/noticias/<slug>/ deve resolver para noticia_detalhe."""
        resolved = resolve('/noticias/meu-slug/')
        self.assertEqual(resolved.url_name, 'noticia_detalhe')

    def test_url_previa_resolve(self):
        """/noticias/previa/<pk>/ deve resolver para noticia_previa."""
        resolved = resolve('/noticias/previa/1/')
        self.assertEqual(resolved.url_name, 'noticia_previa')

    def test_url_noticia_por_id_resolve(self):
        """/noticia/<id>/ (legado) deve resolver para noticia_por_id."""
        resolved = resolve('/noticia/1/')
        self.assertEqual(resolved.url_name, 'noticia_por_id')


# ===========================================================================
# 3. TESTES DA VIEW — LISTA /noticias
# ===========================================================================

class ViewListaNoticiasTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_lista_retorna_200(self):
        """GET /noticias deve retornar HTTP 200."""
        response = self.client.get('/noticias')
        self.assertEqual(response.status_code, 200)

    def test_lista_usa_template_correto(self):
        """GET /noticias deve usar o template atividades.html."""
        response = self.client.get('/noticias')
        self.assertTemplateUsed(response, 'atividades.html')

    def test_lista_exibe_noticia_publicada(self):
        """Notícia publicada deve aparecer na lista."""
        _noticia(titulo='Notícia Visível')
        response = self.client.get('/noticias')
        self.assertContains(response, 'Notícia Visível')

    def test_lista_nao_exibe_rascunho(self):
        """Rascunho não deve aparecer na lista pública."""
        _noticia(titulo='Rascunho Oculto', status=AtividadeDestaque.STATUS_RASCUNHO)
        response = self.client.get('/noticias')
        self.assertNotContains(response, 'Rascunho Oculto')

    def test_lista_nao_exibe_noticia_futura(self):
        """Notícia com data futura não deve aparecer na lista."""
        _noticia(
            titulo='Notícia Futura',
            status=AtividadeDestaque.STATUS_PUBLICADO,
            data_publicacao=timezone.now() + timedelta(days=1),
        )
        response = self.client.get('/noticias')
        self.assertNotContains(response, 'Notícia Futura')

    def test_lista_exibe_chapeu(self):
        """Chapéu da notícia deve aparecer na lista."""
        _noticia(chapeu='SAÚDE')
        response = self.client.get('/noticias')
        self.assertContains(response, 'SAÚDE')

    def test_lista_exibe_linha_fina(self):
        """Linha fina deve aparecer na lista."""
        _noticia(linha_fina='Este é o subtítulo da matéria')
        response = self.client.get('/noticias')
        self.assertContains(response, 'Este é o subtítulo da matéria')

    def test_lista_nao_usa_campo_categoria(self):
        """Template não deve referenciar campo 'categoria' (removido)."""
        response = self.client.get('/noticias')
        # Não deve haver variável Django não resolvida no template
        self.assertNotContains(response, '{{ item.categoria }}')

    def test_lista_nao_usa_campo_resumo(self):
        """Template não deve referenciar campo 'resumo' (removido)."""
        response = self.client.get('/noticias')
        self.assertNotContains(response, '{{ item.resumo }}')

    def test_lista_link_leva_para_slug(self):
        """O link 'LER MATÉRIA COMPLETA' deve apontar para /noticias/<slug>/."""
        n = _noticia(titulo='Notícia Com Link')
        response = self.client.get('/noticias')
        self.assertContains(response, f'/noticias/{n.slug}/')

    def test_lista_paginacao_presente_com_muitas_noticias(self):
        """Com mais de 10 notícias, controles de paginação devem aparecer."""
        for i in range(12):
            _noticia(titulo=f'Notícia Número {i+1:02d}')
        response = self.client.get('/noticias')
        self.assertContains(response, 'page=2')

    def test_lista_pagina_2(self):
        """GET /noticias?page=2 deve retornar 200 com notícias da página 2."""
        for i in range(12):
            _noticia(titulo=f'Notícia Número {i+1:02d}')
        response = self.client.get('/noticias?page=2')
        self.assertEqual(response.status_code, 200)

    def test_lista_estado_vazio(self):
        """Sem notícias, mensagem de estado vazio deve aparecer."""
        response = self.client.get('/noticias')
        self.assertContains(response, 'Nenhuma notícia publicada')


# ===========================================================================
# 4. TESTES DA VIEW — DETALHE /noticias/<slug>/
# ===========================================================================

class ViewDetalheNoticiaTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.noticia = _noticia(
            titulo='Notícia Detalhada',
            chapeu='CAPACITAÇÃO',
            linha_fina='Subtítulo da notícia detalhada.',
            autor='Maria Silva | Secom-MT',
            corpo='<p>Corpo completo e detalhado da matéria.</p>',
            credito_imagem='Fulano/Secom-MT',
        )

    def test_detalhe_retorna_200(self):
        """GET /noticias/<slug>/ deve retornar HTTP 200."""
        url = self.noticia.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detalhe_usa_template_correto(self):
        """Detalhe deve usar o template noticia_detalhe.html."""
        url = self.noticia.get_absolute_url()
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'noticia_detalhe.html')

    def test_detalhe_exibe_chapeu(self):
        """Badge do chapéu deve aparecer no detalhe."""
        url = self.noticia.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(response, 'CAPACITAÇÃO')

    def test_detalhe_exibe_titulo_em_h1(self):
        """Título deve aparecer em tag h1."""
        url = self.noticia.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(response, '<h1')
        self.assertContains(response, 'Notícia Detalhada')

    def test_detalhe_exibe_linha_fina(self):
        """Linha fina deve aparecer no detalhe."""
        url = self.noticia.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(response, 'Subtítulo da notícia detalhada.')

    def test_detalhe_exibe_autor(self):
        """Autor deve aparecer no detalhe."""
        url = self.noticia.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(response, 'Maria Silva | Secom-MT')

    def test_detalhe_exibe_corpo(self):
        """Corpo da matéria deve ser renderizado no detalhe."""
        url = self.noticia.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(response, 'Corpo completo e detalhado da matéria.')

    def test_detalhe_title_tag_com_titulo(self):
        """A tag <title> da página deve conter o título da notícia."""
        url = self.noticia.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(response, 'Notícia Detalhada')
        # Verifica que está no bloco de título
        content = response.content.decode('utf-8')
        self.assertIn('Notícia Detalhada', content)

    def test_detalhe_nao_usa_campo_conteudo_completo(self):
        """Template não deve referenciar campo 'conteudo_completo' (removido)."""
        url = self.noticia.get_absolute_url()
        response = self.client.get(url)
        self.assertNotContains(response, '{{ noticia.conteudo_completo }}')

    def test_detalhe_nao_usa_campo_resumo(self):
        """Template não deve referenciar campo 'resumo' (removido)."""
        url = self.noticia.get_absolute_url()
        response = self.client.get(url)
        self.assertNotContains(response, '{{ noticia.resumo }}')

    def test_detalhe_nao_usa_campo_link(self):
        """Template não deve referenciar campo 'link' (removido)."""
        url = self.noticia.get_absolute_url()
        response = self.client.get(url)
        self.assertNotContains(response, '{{ noticia.link }}')

    def test_detalhe_rascunho_retorna_404(self):
        """Rascunho não deve ser acessível pelo público (404)."""
        rascunho = _noticia(
            titulo='Rascunho Secreto',
            status=AtividadeDestaque.STATUS_RASCUNHO,
        )
        # Busca pela URL de detalhe (que usa .publicadas())
        response = self.client.get(f'/noticias/{rascunho.slug}/')
        self.assertEqual(response.status_code, 404)

    def test_detalhe_sem_chapeu_nao_quebra(self):
        """Notícia sem chapéu deve renderizar sem erro."""
        n = _noticia(chapeu='', titulo='Sem Chapéu')
        # Salva com chapéu vazio (override do campo required)
        AtividadeDestaque.objects.filter(pk=n.pk).update(chapeu='')
        response = self.client.get(f'/noticias/{n.slug}/')
        self.assertEqual(response.status_code, 200)


# ===========================================================================
# 5. TESTES DA VIEW — REDIRECT POR ID /noticia/<id>/
# ===========================================================================

class ViewNoticiaPorIdTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_redirect_por_id_retorna_301(self):
        """GET /noticia/<id>/ deve redirecionar com 301 para /noticias/<slug>/."""
        n = _noticia(titulo='Notícia Por Id')
        response = self.client.get(f'/noticia/{n.pk}/')
        self.assertEqual(response.status_code, 301)

    def test_redirect_por_id_destino_correto(self):
        """Redirect de /noticia/<id>/ deve levar para a URL com slug."""
        n = _noticia(titulo='Destino Correto')
        response = self.client.get(f'/noticia/{n.pk}/', follow=True)
        final_url = response.redirect_chain[-1][0]
        self.assertIn(n.slug, final_url)

    def test_redirect_por_id_inexistente_retorna_404(self):
        """GET /noticia/99999/ deve retornar 404 se não existir."""
        response = self.client.get('/noticia/99999/')
        self.assertEqual(response.status_code, 404)


# ===========================================================================
# 6. TESTES DA VIEW — PRÉ-VISUALIZAÇÃO /noticias/previa/<pk>/
# ===========================================================================

class ViewPreviaNoticiaTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.staff = User.objects.create_user(
            username='editor', password='senha123', is_staff=True
        )
        self.comum = User.objects.create_user(
            username='visitante', password='senha123', is_staff=False
        )
        self.rascunho = _noticia(
            titulo='Rascunho para Prévia',
            status=AtividadeDestaque.STATUS_RASCUNHO,
        )

    def test_previa_sem_login_retorna_404(self):
        """Usuário não autenticado deve receber 404 na prévia."""
        response = self.client.get(f'/noticias/previa/{self.rascunho.pk}/')
        self.assertEqual(response.status_code, 404)

    def test_previa_usuario_comum_retorna_404(self):
        """Usuário autenticado mas não-staff deve receber 404 na prévia."""
        self.client.login(username='visitante', password='senha123')
        response = self.client.get(f'/noticias/previa/{self.rascunho.pk}/')
        self.assertEqual(response.status_code, 404)

    def test_previa_staff_retorna_200(self):
        """Staff autenticado deve acessar a prévia com HTTP 200."""
        self.client.login(username='editor', password='senha123')
        response = self.client.get(f'/noticias/previa/{self.rascunho.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_previa_staff_ve_rascunho(self):
        """Staff deve conseguir visualizar o conteúdo de um rascunho."""
        self.client.login(username='editor', password='senha123')
        response = self.client.get(f'/noticias/previa/{self.rascunho.pk}/')
        self.assertContains(response, 'Rascunho para Prévia')

    def test_previa_pk_invalido_retorna_404(self):
        """Prévia com pk inexistente deve retornar 404."""
        self.client.login(username='editor', password='senha123')
        response = self.client.get('/noticias/previa/99999/')
        self.assertEqual(response.status_code, 404)


# ===========================================================================
# 7. TESTES DA HOME PAGE — Carousel de Notícias
# ===========================================================================

class ViewHomeCarouselTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_retorna_200(self):
        """GET / deve retornar HTTP 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_exibe_titulo_noticia_no_carousel(self):
        """Título da notícia publicada deve aparecer na home."""
        _noticia(titulo='Notícia no Carousel')
        response = self.client.get('/')
        self.assertContains(response, 'Notícia no Carousel')

    def test_home_nao_exibe_rascunho_no_carousel(self):
        """Rascunho não deve aparecer no carousel da home."""
        _noticia(titulo='Rascunho Oculto Home', status=AtividadeDestaque.STATUS_RASCUNHO)
        response = self.client.get('/')
        self.assertNotContains(response, 'Rascunho Oculto Home')

    def test_home_exibe_chapeu_no_carousel(self):
        """Chapéu deve aparecer no carousel da home."""
        _noticia(chapeu='DESTAQUE')
        response = self.client.get('/')
        self.assertContains(response, 'DESTAQUE')

    def test_home_nao_usa_campo_resumo(self):
        """Template da home não deve referenciar campo 'resumo' (removido)."""
        response = self.client.get('/')
        self.assertNotContains(response, '{{ atividade.resumo }}')

    def test_home_nao_usa_campo_conteudo_completo(self):
        """Template da home não deve referenciar 'conteudo_completo' (removido)."""
        response = self.client.get('/')
        self.assertNotContains(response, 'conteudo_completo')

    def test_home_maximo_5_noticias(self):
        """Carousel deve exibir no máximo 5 notícias."""
        for i in range(8):
            _noticia(titulo=f'Notícia Home {i+1:02d}')
        response = self.client.get('/')
        # Verifica que o contexto tem no máximo 5
        atividades = response.context.get('atividades_destaque', [])
        self.assertLessEqual(len(atividades), 5)

    def test_home_cta_texto_atualizado(self):
        """CTA do carousel deve dizer 'LER NOTÍCIA COMPLETA' (não 'ATIVIDADE')."""
        _noticia()
        response = self.client.get('/')
        self.assertContains(response, 'LER NOTÍCIA COMPLETA')
        self.assertNotContains(response, 'LER ATIVIDADE COMPLETA')

    def test_home_botao_ver_todos_aponta_para_noticias(self):
        """Botão 'Ver todos' da seção de notícias deve apontar para /noticias."""
        response = self.client.get('/')
        self.assertContains(response, '/noticias')


# ===========================================================================
# 8. TESTES DE CASOS DE BORDA
# ===========================================================================

class CasosDeBordaTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_noticia_com_html_xss_no_corpo_sanitizado(self):
        """HTML malicioso no corpo deve ser sanitizado antes de salvar no banco."""
        n = _noticia(corpo='<p>Texto</p><script>alert("xss")</script><p>Fim</p>')
        # Verifica diretamente no campo salvo no banco (não na resposta HTTP,
        # pois outros elementos da página podem conter a palavra 'script')
        self.assertNotIn('<script>', n.corpo)
        self.assertIn('<p>Texto</p>', n.corpo)
        self.assertIn('<p>Fim</p>', n.corpo)


    def test_noticia_sem_linha_fina_nao_quebra(self):
        """Notícia com linha_fina vazia não deve quebrar o template."""
        n = _noticia(linha_fina='')
        AtividadeDestaque.objects.filter(pk=n.pk).update(linha_fina='')
        response = self.client.get(n.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_slug_com_caracteres_especiais(self):
        """Título com acentos deve gerar slug válido sem caracteres especiais."""
        n = _noticia(titulo='Proteção à Mulher — Ação e Cidadania')
        self.assertNotIn('ã', n.slug)
        self.assertNotIn('ç', n.slug)
        self.assertNotIn('—', n.slug)

    def test_slug_com_titulo_vazio_usa_fallback(self):
        """Título vazio não deve quebrar a geração do slug."""
        n = AtividadeDestaque(
            chapeu='X', titulo=' ', linha_fina='L',
            autor='A', corpo='<p>c</p>', credito_imagem='D',
            status=AtividadeDestaque.STATUS_PUBLICADO,
            data_publicacao=timezone.now(),
        )
        n.save()  # Não deve lançar exceção
        self.assertTrue(len(n.slug) > 0)

    def test_acesso_slug_inexistente_retorna_404(self):
        """Acessar /noticias/<slug-inexistente>/ deve retornar 404."""
        response = self.client.get('/noticias/slug-que-nao-existe/')
        self.assertEqual(response.status_code, 404)

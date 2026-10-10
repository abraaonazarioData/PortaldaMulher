from django.db import models
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator

class Tema(models.Model):
    nome = models.CharField("Nome do Tema/Seção", max_length=150)
    slug = models.SlugField("Identificador (Slug)", unique=True, help_text="Ex: materiais-educativos, servicos")
    ordem = models.IntegerField("Ordem de Exibição", default=0)

    class Meta:
        verbose_name = "Tema"
        verbose_name_plural = "Temas"
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome

class PageContent(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tema/Seção", related_name="conteudos")
    title = models.CharField("Título", max_length=200)
    slug = models.SlugField("Identificador (Slug)", unique=True, help_text="Ex: sobre-nos, contato. Usado na URL.")
    text = RichTextField("Texto Principal", blank=True)
    reference_sources = models.TextField("Fontes de Referência", blank=True, help_text="Links ou textos de referência.")
    link_url = models.URLField("Link (Botão de Acesso)", blank=True, help_text="URL de destino para botões de acesso.")
    icon = models.CharField("Ícone (FontAwesome)", max_length=100, blank=True, help_text="Ex: fa-solid fa-file-contract")
    image = models.FileField(
        "Imagem",
        upload_to='pages/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','svg','gif'])],
    )
    youtube_video_url = models.URLField("URL do Vídeo do YouTube", blank=True)

    def image_tag(self):
        from django.utils.html import format_html
        if self.image:
            return format_html('<img src="{}" width="150" height="auto" style="border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);" />', self.image.url)
        return "Sem Imagem"
    image_tag.short_description = 'Preview da Imagem'

    @property
    def youtube_id(self):
        import re
        if self.youtube_video_url:
            match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', self.youtube_video_url)
            if match:
                return match.group(1)
        return ''

    @property
    def plain_text_summary(self):
        from django.utils.html import strip_tags
        import html
        text = strip_tags(self.text or '')
        text = html.unescape(text)
        # Removes excess whitespace that might result from stripping tags/entities
        return ' '.join(text.split())

    class Meta:
        verbose_name = "Conteúdo de Página"
        verbose_name_plural = "Conteúdos de Páginas"

    def __str__(self):
        return self.title

class RedeProtecao(models.Model):
    nome = models.CharField("Nome", max_length=255)
    tipo = models.CharField("Tipo", max_length=50, help_text="Ex: DEDM, PMP, NUCLEO")
    cidade = models.CharField("Cidade", max_length=100)
    endereco = models.CharField("Endereço", max_length=255)
    telefone = models.CharField("Telefone", max_length=150, blank=True)
    email = models.EmailField("E-mail", blank=True)
    horario = models.CharField("Horário de Funcionamento", max_length=100, blank=True)
    latitude = models.FloatField("Latitude", null=True, blank=True)
    longitude = models.FloatField("Longitude", null=True, blank=True)

    class Meta:
        verbose_name = "Equipamento da Rede de Proteção"
        verbose_name_plural = "Rede de Proteção"
        ordering = ['cidade', 'nome']

    def __str__(self):
        return f"{self.nome} - {self.cidade}"

class VisitCounter(models.Model):
    count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Contador de Visitas"
        verbose_name_plural = "Contadores de Visitas"

class PanelVisitCounter(models.Model):
    count = models.PositiveIntegerField(default=0)

class PrecisoAjuda(PageContent):
    class Meta:
        proxy = True
        verbose_name = "Preciso de Ajuda (Emergência)"
        verbose_name_plural = "Preciso de Ajuda (Emergência)"

class MateriaisEducativos(PageContent):
    class Meta:
        proxy = True
        verbose_name = "Materiais Educativos"
        verbose_name_plural = "Materiais Educativos"

class PaineisDados(PageContent):
    class Meta:
        proxy = True
        verbose_name = "Painéis e Dados"
        verbose_name_plural = "Painéis e Dados"

class ServicosPublicos(PageContent):
    class Meta:
        proxy = True
        verbose_name = "Serviços e Políticas Públicas"
        verbose_name_plural = "Serviços e Políticas Públicas"

class Legislacao(PageContent):
    class Meta:
        proxy = True
        verbose_name = "Legislação"
        verbose_name_plural = "Legislação"

class SobrePortal(PageContent):
    class Meta:
        proxy = True
        verbose_name = "Rede de Enfrentamento"
        verbose_name_plural = "Rede de Enfrentamento"

class Ouvidoria(PageContent):
    class Meta:
        proxy = True
        verbose_name = "Ouvidoria"
        verbose_name_plural = "Ouvidoria"

class BannerInicial(models.Model):
    titulo = models.CharField("Título (Opcional)", max_length=200, blank=True)
    imagem = models.ImageField("Imagem do Banner", upload_to='banners/')
    link = models.URLField("Link de Destino", blank=True)
    ordem = models.IntegerField("Ordem de Exibição", default=0)
    ativo = models.BooleanField("Ativo?", default=True)

    class Meta:
        verbose_name = "Banner Inicial"
        verbose_name_plural = "Banners Iniciais"
        ordering = ['ordem', '-id']

    def __str__(self):
        return f"Banner {self.id} - {self.titulo or 'Sem Título'}"

class AtividadeDestaque(models.Model):
    titulo = models.CharField("Título da Atividade", max_length=255)
    categoria = models.CharField("Categoria", max_length=100, default="AÇÕES DO GOVERNO")
    resumo = models.TextField("Resumo / Descrição")
    conteudo_completo = RichTextField("Conteúdo Completo", blank=True, null=True, help_text="Se preenchido, cria uma página exclusiva para esta notícia.")
    imagem = models.ImageField("Imagem de Destaque", upload_to='atividades/')
    credito_imagem = models.CharField("Crédito da Imagem (Fotógrafo)", max_length=150, blank=True, null=True)
    autor = models.CharField("Autor da Matéria", max_length=150, blank=True, null=True)
    link = models.URLField("Link da Matéria Completa (Externo)", blank=True, help_text="Use apenas se a matéria for em outro site.")
    data_publicacao = models.DateTimeField("Data de Publicação", auto_now_add=True)
    
    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ['-data_publicacao']

    def __str__(self):
        return self.titulo

class ParceiroInstitucional(models.Model):
    nome = models.CharField("Nome da Instituição", max_length=150)
    logo = models.ImageField("Logo da Instituição", upload_to='parceiros/')
    link = models.URLField("Link do Portal")
    ordem = models.IntegerField("Ordem de Exibição", default=0)

    class Meta:
        verbose_name = "Portal Institucional"
        verbose_name_plural = "Portais Institucionais"
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome

class PlanosMetas(PageContent):
    class Meta:
        proxy = True
        verbose_name = "Planos e Metas"
        verbose_name_plural = "Planos e Metas"

class EstatisticaViolencia(models.Model):
    municipio = models.CharField("Município", max_length=150)
    tipo_crime = models.CharField("Tipo de Crime", max_length=150, help_text="Ex: Feminicídio, Agressão Física, Ameaça")
    ano = models.IntegerField("Ano")
    mes = models.IntegerField("Mês", choices=[(i, str(i)) for i in range(1, 13)], null=True, blank=True)
    quantidade = models.IntegerField("Quantidade de Ocorrências", default=0)
    perfil_vitima_idade = models.CharField("Faixa Etária da Vítima", max_length=50, blank=True, help_text="Ex: 18-25, 26-35")
    perfil_vitima_raca = models.CharField("Raça/Cor da Vítima", max_length=50, blank=True)

    class Meta:
        verbose_name = "Estatística de Violência"
        verbose_name_plural = "Estatísticas de Violência"
        ordering = ['-ano', 'municipio']

    def __str__(self):
        return f"{self.tipo_crime} em {self.municipio} ({self.ano}) - {self.quantidade}"

from django.db import models
from django.utils.timezone import now as timezone_now
from ckeditor.fields import RichTextField
from django_ckeditor_5.fields import CKEditor5Field
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
        validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','webp','gif'])],
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
        indexes = [
            models.Index(fields=['tipo']),
            models.Index(fields=['cidade']),
        ]

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

class NoticiaQuerySet(models.QuerySet):
    def publicadas(self):
        from django.utils import timezone
        return self.filter(status=AtividadeDestaque.STATUS_PUBLICADO, data_publicacao__lte=timezone.now())


# Tags/atributos permitidos no corpo da matéria (sanitização contra XSS)
_CORPO_TAGS = {
    'p', 'br', 'strong', 'b', 'em', 'i', 'u', 's', 'a', 'ul', 'ol', 'li', 'blockquote',
    'h2', 'h3', 'h4', 'figure', 'figcaption', 'img', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'hr', 'span', 'div', 'oembed', 'iframe',
}
_CORPO_ATTRS = {
    '*': {'class', 'style'},
    'a': {'href', 'title', 'target'},
    'img': {'src', 'alt', 'width', 'height', 'srcset', 'sizes'},
    'td': {'colspan', 'rowspan'}, 'th': {'colspan', 'rowspan'},
    'oembed': {'url'},
    'iframe': {'src', 'width', 'height', 'allow', 'allowfullscreen', 'frameborder'},
}


def sanitizar_corpo(html):
    import nh3
    return nh3.clean(
        html or '',
        tags=_CORPO_TAGS,
        attributes=_CORPO_ATTRS,
        url_schemes={'http', 'https', 'mailto'},
        link_rel='noopener noreferrer',
    )


class AtividadeDestaque(models.Model):
    """Notícia publicada integralmente no portal Mulher MT."""
    STATUS_RASCUNHO = 'rascunho'
    STATUS_PUBLICADO = 'publicado'
    STATUS_CHOICES = [(STATUS_RASCUNHO, 'Rascunho'), (STATUS_PUBLICADO, 'Publicado')]

    # Ordem de preenchimento: Chapéu → Título → Linha fina → Autor → Foto → Crédito → Corpo
    chapeu = models.CharField("Chapéu", max_length=40, help_text="Identificação curta do assunto (1 ou 2 palavras). Ex: SAÚDE, CAPACITAÇÃO.")
    titulo = models.CharField("Título", max_length=200, help_text="Manchete principal da notícia.")
    linha_fina = models.TextField("Linha fina", max_length=300, help_text="Subtítulo exibido logo abaixo do título (até 300 caracteres).")
    autor = models.CharField("Autor", max_length=150, help_text="Responsável pela produção da matéria. Ex: Maria Silva | Secom-MT")
    imagem = models.ImageField("Foto de capa", upload_to='atividades/', blank=True, null=True, help_text="Opcional. Foto de destaque exibida no topo da matéria e nos cards de listagem.")
    credito_imagem = models.CharField("Crédito da foto de capa", max_length=150, help_text="Fotógrafo, órgão ou instituição. Ex: Fulano de Tal/Secom-MT")
    corpo = CKEditor5Field("Corpo da matéria", config_name='noticia', help_text="Texto integral. Use o botão de imagem para inserir fotos entre os parágrafos e clique na foto para adicionar legenda e crédito.")

    slug = models.SlugField("Endereço (URL)", max_length=220, unique=True, blank=True, help_text="Gerado automaticamente a partir do título.")
    status = models.CharField("Situação", max_length=10, choices=STATUS_CHOICES, default=STATUS_RASCUNHO)
    data_publicacao = models.DateTimeField("Data de publicação", default=timezone_now, help_text="Datas futuras deixam a notícia agendada.")
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    objects = NoticiaQuerySet.as_manager()

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ['-data_publicacao']
        indexes = [
            models.Index(fields=['status', '-data_publicacao']),
        ]

    def __str__(self):
        return self.titulo

    def _gerar_slug(self):
        from django.utils.text import slugify
        base = slugify(self.titulo)[:200] or 'noticia'
        slug, n = base, 2
        while AtividadeDestaque.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{n}"
            n += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._gerar_slug()
        self.corpo = sanitizar_corpo(self.corpo)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('noticia_detalhe', args=[self.slug])

    @property
    def publicada(self):
        from django.utils import timezone
        return self.status == self.STATUS_PUBLICADO and self.data_publicacao <= timezone.now()

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
        indexes = [
            models.Index(fields=['ano', 'municipio']),
            models.Index(fields=['tipo_crime']),
        ]

    def __str__(self):
        return f"{self.tipo_crime} em {self.municipio} ({self.ano}) - {self.quantidade}"

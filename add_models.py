import os

filepath = r'c:\Users\Administrator\Desktop\Portal Mulher\new\Portal Mulher\django_portal_mulher\core\models.py'
with open(filepath, 'a', encoding='utf-8') as f:
    f.write('''

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
    imagem = models.ImageField("Imagem de Destaque", upload_to='atividades/')
    link = models.URLField("Link da Matéria Completa", blank=True)
    data_publicacao = models.DateTimeField("Data de Publicação", auto_now_add=True)
    
    class Meta:
        verbose_name = "Atividade em Destaque"
        verbose_name_plural = "Atividades em Destaque"
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

class LegislacaoDestaque(PageContent):
    class Meta:
        proxy = True
        verbose_name = "Card de Legislação (Página Inicial)"
        verbose_name_plural = "Cards de Legislação (Página Inicial)"
''')
print('Models appended successfully.')

"""
Reestrutura o módulo de Notícias (AtividadeDestaque):
  categoria         -> chapeu
  resumo            -> linha_fina
  conteudo_completo -> corpo   (CKEditor 5)
  link (externo)    -> removido; quando existia, vira "Fonte original" ao final do corpo
Adiciona slug, status (rascunho/publicado), data editável e auditoria.
Notícias existentes são marcadas como "publicado" para continuarem visíveis.
"""
import django.utils.timezone
import django_ckeditor_5.fields
from django.db import migrations, models
from django.utils.html import escape
from django.utils.text import slugify


def copiar_dados(apps, schema_editor):
    Noticia = apps.get_model('core', 'AtividadeDestaque')
    usados = set()
    for n in Noticia.objects.all():
        n.chapeu = (n.categoria or 'NOTÍCIAS')[:40]
        n.linha_fina = (n.resumo or '')[:300]
        corpo = n.conteudo_completo or ''
        if not corpo.strip():
            corpo = f"<p>{escape(n.resumo or '')}</p>"
        if n.link:
            link = escape(n.link)
            corpo += f'<p><em>Fonte original: <a href="{link}" target="_blank" rel="noopener noreferrer">{link}</a></em></p>'
        n.corpo = corpo
        n.autor = n.autor or 'Mulher MT'
        n.credito_imagem = n.credito_imagem or 'Divulgação'

        base = slugify(n.titulo)[:200] or 'noticia'
        slug, i = base, 2
        while slug in usados:
            slug = f"{base}-{i}"
            i += 1
        usados.add(slug)
        n.slug = slug
        n.status = 'publicado'
        n.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_atividadedestaque_autor_and_more'),
    ]

    operations = [
        # 1) Novos campos (temporariamente permissivos)
        migrations.AddField('atividadedestaque', 'chapeu', models.CharField(default='', max_length=40, verbose_name='Chapéu')),
        migrations.AddField('atividadedestaque', 'linha_fina', models.TextField(default='', max_length=300, verbose_name='Linha fina')),
        migrations.AddField('atividadedestaque', 'corpo', django_ckeditor_5.fields.CKEditor5Field(default='', verbose_name='Corpo da matéria')),
        migrations.AddField('atividadedestaque', 'slug', models.SlugField(max_length=220, null=True, blank=True)),
        migrations.AddField('atividadedestaque', 'status', models.CharField(default='publicado', max_length=10)),
        migrations.AddField('atividadedestaque', 'criado_em', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Criado em'), preserve_default=False),
        migrations.AddField('atividadedestaque', 'atualizado_em', models.DateTimeField(auto_now=True, verbose_name='Atualizado em')),

        # 2) Migração dos dados
        migrations.RunPython(copiar_dados, migrations.RunPython.noop),

        # 3) Remoção dos campos antigos
        migrations.RemoveField('atividadedestaque', 'categoria'),
        migrations.RemoveField('atividadedestaque', 'resumo'),
        migrations.RemoveField('atividadedestaque', 'conteudo_completo'),
        migrations.RemoveField('atividadedestaque', 'link'),

        # 4) Regras definitivas
        migrations.AlterField('atividadedestaque', 'chapeu', models.CharField(help_text='Identificação curta do assunto (1 ou 2 palavras). Ex: SAÚDE, CAPACITAÇÃO.', max_length=40, verbose_name='Chapéu')),
        migrations.AlterField('atividadedestaque', 'titulo', models.CharField(help_text='Manchete principal da notícia.', max_length=200, verbose_name='Título')),
        migrations.AlterField('atividadedestaque', 'linha_fina', models.TextField(help_text='Subtítulo exibido logo abaixo do título (até 300 caracteres).', max_length=300, verbose_name='Linha fina')),
        migrations.AlterField('atividadedestaque', 'autor', models.CharField(help_text='Responsável pela produção da matéria. Ex: Maria Silva | Secom-MT', max_length=150, verbose_name='Autor')),
        migrations.AlterField('atividadedestaque', 'imagem', models.ImageField(upload_to='atividades/', verbose_name='Foto de capa')),
        migrations.AlterField('atividadedestaque', 'credito_imagem', models.CharField(help_text='Fotógrafo, órgão ou instituição. Ex: Fulano de Tal/Secom-MT', max_length=150, verbose_name='Crédito da foto de capa')),
        migrations.AlterField('atividadedestaque', 'corpo', django_ckeditor_5.fields.CKEditor5Field(help_text='Texto integral. Use o botão de imagem para inserir fotos entre os parágrafos e clique na foto para adicionar legenda e crédito.', verbose_name='Corpo da matéria')),
        migrations.AlterField('atividadedestaque', 'slug', models.SlugField(blank=True, help_text='Gerado automaticamente a partir do título.', max_length=220, unique=True, verbose_name='Endereço (URL)')),
        migrations.AlterField('atividadedestaque', 'status', models.CharField(choices=[('rascunho', 'Rascunho'), ('publicado', 'Publicado')], default='rascunho', max_length=10, verbose_name='Situação')),
        migrations.AlterField('atividadedestaque', 'data_publicacao', models.DateTimeField(default=django.utils.timezone.now, help_text='Datas futuras deixam a notícia agendada.', verbose_name='Data de publicação')),
    ]

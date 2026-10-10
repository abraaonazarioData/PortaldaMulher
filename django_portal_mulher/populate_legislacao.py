import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_django.settings')
django.setup()

from core.models import Tema, PageContent

def populate():
    # Garantir que o Tema "Legislação" existe
    tema, created = Tema.objects.get_or_create(
        slug='legislacao',
        defaults={'nome': 'Legislação', 'ordem': 5}
    )

    items = [
        {
            "title": "Lei Complementar Estadual 837/2026",
            "text": "Institui o Gabinete de Enfrentamento à Violência de Gênero contra a Mulher (GEVM) no âmbito de Mato Grosso.",
            "link_url": "https://www.sefaz.mt.gov.br/legislacao/pesquisa-normas"
        },
        {
            "title": "Plano Estadual de Metas (2025)",
            "text": "Plano Estadual de Metas para o Enfrentamento da Violência Doméstica e Familiar contra a Mulher.",
            "link_url": "#"
        },
        {
            "title": "Lei Federal 11.340/2006 (Lei Maria da Penha)",
            "text": "Dispõe mecanismos para coibir a violência doméstica e familiar contra a mulher.",
            "link_url": "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2006/lei/l11340.htm"
        }
    ]

    for item in items:
        slug = slugify(item['title'])
        PageContent.objects.update_or_create(
            slug=slug,
            defaults={
                'tema': tema,
                'title': item['title'],
                'text': item['text'],
                'link_url': item['link_url']
            }
        )
    print("Dados de Legislação inseridos com sucesso!")

if __name__ == '__main__':
    populate()

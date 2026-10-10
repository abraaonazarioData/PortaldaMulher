import os
import django
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_django.settings')
django.setup()

from core.models import PageContent, Tema

def get_or_create_tema(nome, slug):
    tema, _ = Tema.objects.get_or_create(slug=slug, defaults={'nome': nome})
    return tema

def populate():
    # 1. Preciso de Ajuda
    tema_ajuda = get_or_create_tema('Preciso de Ajuda', 'preciso-de-ajuda')
    ajudas = [
        {"title": "Polícia Militar", "text": "24h Emergências", "icon": "190", "link": "tel:190"},
        {"title": "Polícia Civil", "text": "Denúncias Anônimas", "icon": "197", "link": "tel:197"},
        {"title": "SAMU", "text": "Urgências Médicas", "icon": "192", "link": "tel:192"},
        {"title": "Central da Mulher", "text": "Atendimento 24h", "icon": "180", "link": "tel:180"},
    ]
    for item in ajudas:
        PageContent.objects.update_or_create(
            slug=slugify(item['title']),
            defaults={
                'tema': tema_ajuda,
                'title': item['title'],
                'text': item['text'],
                'icon': item['icon'],
                'link_url': item['link'],
            }
        )

    # 2. Serviços e Políticas Públicas
    tema_servicos = get_or_create_tema('Serviços e Políticas Públicas', 'servicos-e-politicas-publicas')
    servicos = [
        {"title": "Abrir ocorrências", "text": "Link direto para registro de ocorrência online e pedido de medida protetiva pela internet.", "link": "https://delegaciadigital.pjc.mt.gov.br/", "icon": "fa-solid fa-laptop-medical"},
        {"title": "Meninas que Transformam", "text": "Programa para apoiar o desenvolvimento, a autonomia e a preparação de jovens e adolescentes para o mercado de trabalho.", "link": "https://seletivo.seplag.mt.gov.br/detalhes/53?slug=pss-programa-meninas-que-transformam-2026", "icon": "fa-solid fa-graduation-cap"},
        {"title": "Patrulha Maria da Penha", "text": "Garantir a segurança da mulher e eficácia das medidas protetivas de urgência que o agressor deve cumprir.", "link": "https://www.pm.mt.gov.br/pmp", "icon": "fa-solid fa-shield-halved"},
    ]
    for item in servicos:
        PageContent.objects.update_or_create(
            slug=slugify(item['title']),
            defaults={
                'tema': tema_servicos,
                'title': item['title'],
                'text': item['text'],
                'link_url': item['link'],
                'icon': item['icon'],
            }
        )

    # 3. Painéis e Dados
    tema_paineis = get_or_create_tema('Painéis e Dados', 'paineis-e-dados')
    PageContent.objects.update_or_create(
        slug='painel-de-monitoramento',
        defaults={
            'tema': tema_paineis,
            'title': 'Painel de Monitoramento',
            'text': 'Acompanhe o painel de monitoramento oficial com a análise detalhada dos índices de violência contra a mulher no Estado de Mato Grosso. Os dados são fornecidos pela Secretaria Adjunta de Inteligência (SESP).',
            'link_url': 'https://www.mulher.mt.gov.br/estatisticas',
        }
    )

    # 4. Materiais Educativos (Videos)
    tema_videos = get_or_create_tema('Materiais Educativos', 'materiais-educativos')
    videos = [
        {"url": "https://youtu.be/infxV6ejKMc", "title": "O que é violência de gênero contra a mulher e seus tipos"},
        {"url": "https://www.youtube.com/watch?v=YkYNlkr1FQE", "title": "O fenômeno do ciclo da violência"},
        {"url": "https://www.youtube.com/shorts/-PPR-6kczH0", "title": "Os mecanismos para rompimento do ciclo de violência"},
        {"url": "https://youtu.be/F6epuxrqWW0", "title": "Encaminhamentos para a rede de proteção"},
        {"url": "https://youtube.com/shorts/I_K9iL2wkFA?feature=share", "title": "Quem procurar em caso de violência doméstica e familiar"},
        {"url": "https://youtube.com/shorts/r2JFHZ6k2dE", "title": "A importância de buscar ajuda e responsabilidade de familiares e amigos próximos"},
        {"url": "https://www.youtube.com/watch?v=4wSwnrVCDJI", "title": "O autor não cumpre as medidas protetivas, o que devo fazer?"},
        {"url": "https://youtube.com/shorts/rkon1vL77K0?feature=share", "title": "A quem se destina e como buscar"},
        {"url": "https://youtube.com/shorts/HRusxXexTEo?feature=share", "title": "Qual a diferença entre o APP SOS Mulher e a tornozeleira eletrônica?"},
        {"url": "https://youtube.com/shorts/l-JWRXDxv8A?feature=share", "title": "Preciso ter filmagens, documentação ou testemunhas para buscar ajuda?"},
        {"url": "https://youtu.be/uzbAXbB_ePc", "title": "Consequências legais da violência contra a mulher"}
    ]
    for i, v in enumerate(videos, start=1):
        PageContent.objects.update_or_create(
            slug=f'video-{i}',
            defaults={
                'tema': tema_videos,
                'title': v['title'],
                'youtube_video_url': v['url'],
            }
        )
        
    print("Conteúdos do front-end migrados para o banco de dados com sucesso!")

if __name__ == '__main__':
    populate()

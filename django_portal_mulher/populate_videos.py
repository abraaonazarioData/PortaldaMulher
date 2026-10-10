import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_django.settings')
django.setup()

from core.models import PageContent

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

# Deletar existentes para não duplicar se rodar duas vezes
PageContent.objects.filter(slug__startswith='video-').delete()

for i, v in enumerate(videos, start=1):
    PageContent.objects.create(
        title=v['title'],
        slug=f'video-{i}',
        youtube_video_url=v['url']
    )

print("Vídeos importados com sucesso!")

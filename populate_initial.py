import os, sys, urllib.request
import django
from django.core.files.base import ContentFile

sys.path.append(r'c:\Users\Administrator\Desktop\Portal Mulher\new\Portal Mulher\django_portal_mulher')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_django.settings')
django.setup()

from core.models import AtividadeDestaque, ParceiroInstitucional, PageContent, Tema

print('Populating Atividade Destaque...')
if not AtividadeDestaque.objects.exists():
    img_url = 'https://ceia.mt.gov.br/media/publicacoes/Pal%C3%A1cio_Paiagu%C3%A1s.jpg'
    req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        img_content = urllib.request.urlopen(req).read()
    except Exception as e:
        print('Failed to download original image, using fallback.')
        img_content = urllib.request.urlopen('https://placehold.co/600x400.jpg').read()
    
    atividade = AtividadeDestaque(
        titulo='Governo de MT lança novo programa de proteção integral no Estado',
        categoria='Ações do Governo',
        resumo='Com o objetivo de fortalecer a rede de apoio, o Governo de Mato Grosso lança novas medidas que visam garantir a segurança, autonomia e capacitação das mulheres em todas as regiões, unificando os atendimentos...',
        link='https://www.seplag.mt.gov.br/web/mt/w/governo-de-mt-suspende-not%C3%ADcias-institucionais-do-portal-em-cumprimento-%C3%A0s-normas-eleitorais'
    )
    atividade.imagem.save('palacio.jpg', ContentFile(img_content))
    atividade.save()
    print('Atividade created.')

print('Populating Parceiros Institucionais...')
if not ParceiroInstitucional.objects.exists():
    parceiros = [
        ('SECOM', 'https://www.mt.gov.br/mtgov-theme/images/brasao.png', 'http://www.secom.mt.gov.br/', 1),
        ('SEPLAG', 'https://www.seplag.mt.gov.br/seplag-theme/images/brasao.png', 'http://www.seplag.mt.gov.br/', 2),
        ('SESP', 'https://www.sesp.mt.gov.br/sesp-theme/images/brasao.png', 'http://www.sesp.mt.gov.br/', 3),
        ('CASA CIVIL', 'https://www.casacivil.mt.gov.br/casacivil-theme/images/brasao.png', 'http://www.casacivil.mt.gov.br/', 4),
    ]
    for nome, img_url, link, ordem in parceiros:
        try:
            req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            img_content = urllib.request.urlopen(req).read()
            p = ParceiroInstitucional(nome=nome, link=link, ordem=ordem)
            p.logo.save(f'{nome.lower().replace(" ", "_")}.png', ContentFile(img_content))
            p.save()
            print(f'Parceiro {nome} created.')
        except Exception as e:
            print(f'Error saving {nome}: {e}')

print('Populating Planos e Metas...')
tema, _ = Tema.objects.get_or_create(nome='Planos e Metas', slug='planos-e-metas')
if not PageContent.objects.filter(tema=tema).exists():
    p = PageContent(
        tema=tema,
        title='Planos e Metas',
        slug='planos-metas-home',
        text='<p>O Portal Mato Grosso se dedica à proteção da mulher no Estado, buscando o cumprimento dos objetivos e metas estabelecidos pela Secretaria de Estado de Segurança Pública e por todos os órgãos da Rede de Proteção.</p><p><strong>Nosso objetivo central:</strong> erradicar a violência e promover a autonomia.</p>'
    )
    p.save()
    print('Planos e Metas created.')

print('Done.')

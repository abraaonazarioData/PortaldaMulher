import os
import sys
import django

sys.path.append(r'c:\Users\Administrator\Desktop\Portal Mulher\new\Portal Mulher\django_portal_mulher')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_django.settings')
django.setup()

from core.models import Tema, PageContent

tema_rede, _ = Tema.objects.get_or_create(slug='sobre-o-portal', defaults={'nome': 'Sobre o Portal'})

html_text = """
<p class="pmg-content-text">
    A violência contra a mulher é um fenômeno complexo que exige atuação conjunta do Estado e da sociedade. Por isso, Mato Grosso instituiu, por meio do Decreto Estadual nº 1.708/2025, a Rede Estadual de Enfrentamento à Violência contra a Mulher (REDEVIM), com a missão de planejar, acompanhar e implementar ações voltadas ao enfrentamento da violência contra as mulheres.
</p>
<p class="pmg-content-text">
    A REDEVIM funciona de forma integrada, com participação de diferentes instituições e áreas de governo: Gabinete de Enfrentamento à Violência de Gênero contra a Mulher (GEVM); Secretaria de Estado de Segurança Pública (SESP); Secretaria de Estado de Assistência Social (SETASC); Secretaria de Estado de Saúde (SES); Secretaria de Estado de Educação (SEDUC); Secretaria de Estado de Justiça (SEJUS); Secretaria de Estado de Comunicação (SECOM); Polícia Judiciária Civil; Polícia Militar; Perícia Oficial e Identificação Técnica (POLITEC); Corpo de Bombeiros Militar; Secretaria de Estado de Cultura, Esporte e Lazer (SECEL), e, mediante adesão, Assembleia Legislativa de Mato Grosso; Tribunal de Justiça; Tribunal de Contas; Ministério Público; Defensoria Pública; Ordem dos Advogados do Brasil – Seccional Mato Grosso; e Conselho Estadual dos Direitos da Mulher.
</p>
<p class="pmg-content-text">
    A REDEVIM possui estrutura colegiada, de natureza consultiva e deliberativa, composta por Coordenação (Gabinete de Enfrentamento à Violência de Gênero contra a Mulher – GEVM), Plenária (formada pelos representantes das instituições integrantes) e Secretaria-Executiva.
</p>
<p class="pmg-content-text">
    As reuniões ordinárias são realizadas mensalmente e podem ocorrer presencialmente ou por videoconferência, observadas as regras previstas no Regimento Interno.
</p>
<h2 class="pmg-sub-header">Normativos</h2>
<ul style="margin-left: 20px; margin-bottom: 20px; line-height: 1.6; color: var(--pmg-text, #333);">
    <li>Decreto...</li>
    <li>Resoluções...</li>
</ul>
<h2 class="pmg-sub-header">Governança</h2>
<ul style="margin-left: 20px; margin-bottom: 20px; line-height: 1.6; color: var(--pmg-text, #333);">
    <li>Calendário de reuniões</li>
    <li>Reuniões</li>
    <li>Grupos de Trabalho</li>
</ul>
<h2 class="pmg-sub-header">Publicações</h2>
<div style="margin-bottom: 20px; line-height: 1.6; color: var(--pmg-text, #333);">
    Publicações
</div>
<aside class="pmg-highlight-aside">
    Nesse contexto, a <strong>Rede Estadual de Enfrentamento</strong> exerce papel central de consolidação dos dados relacionados ao enfrentamento da violência e articulação permanente entre os órgãos, coordenando a integração das informações e promovendo o aprimoramento contínuo das ações.
    <div style="margin-top: 20px; text-align: center;">
        <p style="font-size: 0.95rem; margin-bottom: 10px;">Ficou com alguma dúvida ou precisa falar com nossa equipe?</p>
        <span style="display: inline-block; background-color: #ffdf00; color: #002b5e; padding: 10px 25px; border-radius: 6px; text-decoration: none; font-weight: 700;">
            <i class="fa-regular fa-envelope"></i> gabinetemulher@casacivil.mt.gov.br
        </span>
    </div>
</aside>
"""

if not PageContent.objects.filter(tema=tema_rede).exists():
    PageContent.objects.create(
        tema=tema_rede,
        title='Rede Estadual de Enfrentamento à Violência contra a Mulher',
        text=html_text
    )
    print('Created Rede de Enfrentamento!')
else:
    print('Already exists!')

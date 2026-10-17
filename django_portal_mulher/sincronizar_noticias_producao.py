#!/usr/bin/env python
"""
Script de sincronização de notícias de produção para o Portal Mulher MT.
Baixa as imagens oficiais de https://mulher.mt.gov.br/media/atividades/
e cadastra as 5 matérias completas no modelo AtividadeDestaque.
"""
import os
import sys
import django
import urllib.request
import urllib.parse
from datetime import datetime
from django.utils import timezone
import zoneinfo

# Configura ambiente Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_django.settings')
django.setup()

from core.models import AtividadeDestaque

MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'atividades')
os.makedirs(MEDIA_DIR, exist_ok=True)

tz_cuiaba = zoneinfo.ZoneInfo("America/Cuiaba")

NOTICIAS = [
    {
        'titulo': 'PM liberta mulher mantida em cárcere privado por 30 dias',
        'chapeu': 'COMBATE À VIOLÊNCIA',
        'linha_fina': 'Vítima relatou agressões e violência sexual durante o período em que foi mantida presa pelo namorado, detido em flagrante.',
        'autor': 'Polícia Militar de Mato Grosso | PMMT',
        'credito_imagem': 'Assessoria | PMMT',
        'img_filename': 'viatura_pm_mt_1.jpg',
        'img_url': 'https://mulher.mt.gov.br/media/atividades/viatura_pm_mt_1.jpg',
        'data_publicacao': datetime(2026, 10, 15, 20, 52, tzinfo=tz_cuiaba),
        'corpo': """<p>A Polícia Militar de Mato Grosso libertou, nesta quinta-feira (15.10), uma mulher que vinha sendo mantida em cárcere privado por aproximadamente 30 dias pelo companheiro.</p>
<p>A equipe policial foi acionada após denúncias anônimas informando sobre a situação de confinamento e agressões no imóvel. No local, a guarnição constatou a veracidade dos fatos e realizou a abordagem tática, conseguindo resgatar a vítima com segurança.</p>
<p>Em seu depoimento preliminar, a vítima relatou ter sofrido agressões físicas constantes e violência psicológica ao longo de todo o período em que permaneceu impedida de sair ou fazer contato com familiares. O suspeito foi preso em flagrante delito e encaminhado à Delegacia Especializada de Defesa da Mulher para as providências legais.</p>
<p>A vítima recebeu acolhimento humanizado e foi encaminhada para atendimento médico e acompanhamento pela rede socioassistencial e psicológica do Estado.</p>"""
    },
    {
        'titulo': 'Corpo de Bombeiros promove curso para qualificar atendimento a mulheres vítimas de violência',
        'chapeu': 'ENFRENTAMENTO À VIOLÊNCIA',
        'linha_fina': 'Capacitação aborda acolhimento, procedimentos de atendimento e encaminhamento das vítimas à rede de proteção em Mato Grosso.',
        'autor': 'Corpo de Bombeiros Militar | CBMMT',
        'credito_imagem': 'Assessoria | CBMMT',
        'img_filename': 'CAMVV3.jpg',
        'img_url': 'https://mulher.mt.gov.br/media/atividades/CAMVV3.jpg',
        'data_publicacao': datetime(2026, 10, 15, 10, 30, tzinfo=tz_cuiaba),
        'corpo': """<p>O Corpo de Bombeiros Militar de Mato Grosso (CBMMT) iniciou nesta semana o Curso de Aperfeiçoamento para o Atendimento a Mulheres em Situação de Violência (CAMVV), voltado para bombeiros militares que atuam no serviço operacional e de resgate.</p>
<p>O objetivo é capacitar a tropa para reconhecer sinais de violência doméstica, prestar os primeiros socorros de maneira humanizada, evitar a revitimização e realizar o correto encaminhamento das mulheres para as delegacias e abrigos da rede de proteção do Estado.</p>
<p>A formação integra o conjunto de ações integradas do Governo de Mato Grosso para intensificar a resposta estatal no combate à violência de gênero e o fortalecimento de protocolos de acolhimento emergencial.</p>"""
    },
    {
        'titulo': 'Polícia Civil prende homem investigado por ameaça contra companheira e posse ilegal de arma de fogo',
        'chapeu': 'VIOLÊNCIA DOMÉSTICA',
        'linha_fina': 'Suspeito havia sido solto após audiência de custódia, mas voltou a ser preso após diligências realizadas durante o feriado prolongado.',
        'autor': 'Polícia Judiciária Civil | PJCMT',
        'credito_imagem': 'Assessoria | PJCMT',
        'img_filename': 'Delegacia_de_Araputanga.jpeg',
        'img_url': 'https://mulher.mt.gov.br/media/atividades/Delegacia_de_Araputanga.jpeg',
        'data_publicacao': datetime(2026, 10, 15, 9, 47, tzinfo=tz_cuiaba),
        'corpo': """<p>A Polícia Judiciária Civil de Mato Grosso cumpriu mandado de prisão preventiva contra um indivíduo investigado por crimes de ameaça no âmbito da Lei Maria da Penha e posse ilegal de arma de fogo.</p>
<p>O suspeito havia sido inicialmente detido, mas obteve liberdade provisória durante audiência de custódia. No entanto, novas diligências da equipe investigativa demonstraram descumprimento iminente de medidas cautelares e risco à integridade da vítima.</p>
<p>Diante dos novos elementos apresentados pela autoridade policial, o Poder Judiciário decretou a prisão preventiva, que foi imediatamente cumprida. O investigado foi recolhido à unidade prisional e permanece à disposição da Justiça.</p>"""
    },
    {
        'titulo': 'Escola de Saúde Pública promove curso de boas práticas no pré-natal, parto e nascimento',
        'chapeu': 'AÇÕES DO GOVERNO',
        'linha_fina': 'Médicos, enfermeiros e gestores da Baixada Cuiabana passam por formação de 30 horas para melhoria da Rede Alyne e a atenção à saúde das mulheres.',
        'autor': 'Secom-MT | SES-MT',
        'credito_imagem': 'Secom-MT',
        'img_filename': 'Foto_praticas_pre-Natal.jpg',
        'img_url': 'https://mulher.mt.gov.br/media/atividades/Foto_pr%C3%A1ticas_pr%C3%A9-Natal.jpg',
        'data_publicacao': datetime(2026, 10, 15, 9, 43, tzinfo=tz_cuiaba),
        'corpo': """<p>A Escola de Saúde Pública do Estado de Mato Grosso promoveu uma capacitação estratégica de boas práticas na atenção ao pré-natal, parto e puerpério, reunindo médicos, enfermeiros e equipes multiprofissionais de saúde da Baixada Cuiabana.</p>
<p>A qualificação abrange 30 horas de treinamento prático e teórico com foco na redução da mortalidade materna e neonatal, na ampliação da assistência qualificada e na consolidação das diretrizes da Rede Alyne em todo o território mato-grossense.</p>
<p>Segundo a Secretaria de Estado de Saúde (SES-MT), o aprimoramento contínuo dos profissionais da ponta é essencial para garantir um atendimento seguro, digno e humanizado a todas as mães e bebês atendidos pelo Sistema Único de Saúde (SUS).</p>"""
    },
    {
        'titulo': 'Polícia Civil prende três homens por agredir mulher em Rondonópolis',
        'chapeu': 'VIOLÊNCIA CONTRA A MULHER',
        'linha_fina': 'A ação ocorreu após a vítima ser agredida e ameaçada por cobrança de aluguéis atrasados dos suspeitos.',
        'autor': 'Polícia Judiciária Civil | PJCMT',
        'credito_imagem': 'Assessoria | PJCMT',
        'img_filename': 'Delegacia_da_Mulher_de_Rondonopolis.jpg',
        'img_url': 'https://mulher.mt.gov.br/media/atividades/Delegacia_da_Mulher_de_Rondon%C3%B3polis.jpg',
        'data_publicacao': datetime(2026, 10, 15, 9, 40, tzinfo=tz_cuiaba),
        'corpo': """<p>A Delegacia Especializada de Defesa da Mulher (DEDM) de Rondonópolis efetuou a prisão em flagrante de três homens envolvidos em graves agressões físicas e ameaças contra uma mulher.</p>
<p>Conforme as apurações, o crime foi motivado por cobranças arbitrárias e desavenças contratuais. A vítima foi encurralada e agredida, sofrendo lesões corporais antes de conseguir acionar o socorro policial.</p>
<p>Os policiais civis localizaram e detiveram os agressores ainda nas proximidades. Todos foram autuados pelos crimes correspondentes e autuados conforme a legislação vigente, resguardando a segurança física da vítima.</p>"""
    }
]

def baixar_imagem(url, destino):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response, open(destino, 'wb') as out_file:
            out_file.write(response.read())
        print(f"  [OK] Imagem baixada: {os.path.basename(destino)}")
        return True
    except Exception as e:
        print(f"  [AVISO] Falha ao baixar {url}: {e}")
        return False

def executar_sincronizacao():
    print("=== Sincronizando 5 Notícias Oficiais da Produção ===")
    
    total_criadas = 0
    total_atualizadas = 0
    
    for item in NOTICIAS:
        caminho_local_img = os.path.join(MEDIA_DIR, item['img_filename'])
        rel_img_path = f"atividades/{item['img_filename']}"
        
        # Baixa imagem se ainda não existir
        if not os.path.exists(caminho_local_img):
            baixar_imagem(item['img_url'], caminho_local_img)
            
        # Busca notícia pelo título ou cria nova
        noticia = AtividadeDestaque.objects.filter(titulo=item['titulo']).first()
        if not noticia:
            noticia = AtividadeDestaque(titulo=item['titulo'])
            total_criadas += 1
            status_txt = "Criada"
        else:
            total_atualizadas += 1
            status_txt = "Atualizada"
            
        noticia.chapeu = item['chapeu']
        noticia.linha_fina = item['linha_fina']
        noticia.autor = item['autor']
        noticia.credito_imagem = item['credito_imagem']
        noticia.corpo = item['corpo']
        noticia.status = AtividadeDestaque.STATUS_PUBLICADO
        noticia.data_publicacao = item['data_publicacao']
        
        if os.path.exists(caminho_local_img):
            noticia.imagem = rel_img_path
            
        noticia.save()
        print(f"-> Notícia {status_txt}: '{noticia.titulo}' (Slug: {noticia.slug})")

    print(f"\nResultado da Sincronização:")
    print(f"- Total no banco agora: {AtividadeDestaque.objects.count()} matérias.")
    print(f"- Criadas: {total_criadas} | Atualizadas: {total_atualizadas}")

if __name__ == '__main__':
    executar_sincronizacao()

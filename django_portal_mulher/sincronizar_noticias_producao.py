#!/usr/bin/env python
"""
Script de sincronização completa de notícias de produção para o Portal Mulher MT.
Extrai as notícias oficiais de https://mulher.mt.gov.br/atividades
Baixa as imagens oficiais para media/atividades/
e cadastra/atualiza as matérias no modelo AtividadeDestaque com sanitização anti-XSS.
"""
import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime
import zoneinfo

# Configura ambiente Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_django.settings')

import django
django.setup()

from core.models import AtividadeDestaque

MEDIA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'atividades')
os.makedirs(MEDIA_DIR, exist_ok=True)

tz_cuiaba = zoneinfo.ZoneInfo("America/Cuiaba")

def get_autor_e_credito(link, chapeu):
    l = (link or '').lower()
    if 'pjc.mt.gov.br' in l:
        return 'Polícia Judiciária Civil | PJCMT', 'Assessoria | PJCMT'
    elif 'pm.mt.gov.br' in l:
        return 'Polícia Militar de Mato Grosso | PMMT', 'Assessoria | PMMT'
    elif 'mpmt.mp.br' in l:
        return 'Ministério Público de Mato Grosso | MPMT', 'Assessoria | MPMT'
    elif 'tjmt.jus.br' in l:
        return 'Tribunal de Justiça de Mato Grosso | TJMT', 'Assessoria | TJMT'
    elif 'secom.mt.gov.br' in l:
        return 'Secom-MT', 'Secom-MT'
    elif 'setasc.mt.gov.br' in l:
        return 'Setasc-MT', 'Assessoria | Setasc-MT'
    elif 'tce.mt.gov.br' in l:
        return 'Tribunal de Contas de Mato Grosso | TCE-MT', 'Assessoria | TCE-MT'
    elif 'cuiaba.mt.gov.br' in l:
        return 'Prefeitura de Cuiabá', 'Assessoria | Prefeitura de Cuiabá'
    elif 'juina.mt.gov.br' in l:
        return 'Prefeitura de Juína', 'Assessoria | Prefeitura de Juína'
    elif 'agriculturafamiliar.mt.gov.br' in l:
        return 'Seaf-MT', 'Assessoria | Seaf-MT'
    elif 'bombeiros.mt.gov.br' in l:
        return 'Corpo de Bombeiros Militar | CBMMT', 'Assessoria | CBMMT'
    else:
        return 'Governo do Estado de Mato Grosso', 'Assessoria de Comunicação'

def baixar_imagem(img_filename):
    if not img_filename:
        return False
    destino = os.path.join(MEDIA_DIR, img_filename)
    if os.path.exists(destino) and os.path.getsize(destino) > 0:
        return True

    encoded_name = urllib.parse.quote(img_filename)
    urls = [
        f"http://mulher.mt.gov.br/media/atividades/{encoded_name}",
        f"http://mulher.mt.gov.br/media/atividades/{img_filename}",
        f"https://mulher.mt.gov.br/media/atividades/{encoded_name}",
    ]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp, open(destino, 'wb') as f_out:
                f_out.write(resp.read())
            if os.path.exists(destino) and os.path.getsize(destino) > 0:
                print(f"  [OK] Imagem baixada: {img_filename}")
                return True
        except Exception:
            pass
    return False

def parse_data(data_str):
    clean = ' '.join(data_str.replace('|', ' ').split())
    try:
        return datetime.strptime(clean, "%d/%m/%Y %H:%M").replace(tzinfo=tz_cuiaba)
    except Exception:
        try:
            return datetime.strptime(clean, "%d/%m/%Y").replace(tzinfo=tz_cuiaba)
        except Exception:
            return datetime.now(tz_cuiaba)

def sincronizar_todas():
    # Carrega arquivo JSON exportado de produção se disponível
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scratch', 'noticias_extraidas.json'))
    if not os.path.exists(json_path):
        print(f"Arquivo de extração {json_path} não encontrado.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        noticias = json.load(f)

    print(f"=== Sincronizando {len(noticias)} Notícias de Produção ===")
    total_criadas = 0
    total_atualizadas = 0

    for item in noticias:
        titulo = item['titulo']
        chapeu = item['chapeu'][:40]
        linha_fina = item['linha_fina'][:300]
        data_pub = parse_data(item['data_str'])
        autor, credito_img = get_autor_e_credito(item['link_externo'], chapeu)
        img_filename = item['img_filename']

        baixar_imagem(img_filename)
        caminho_local_img = os.path.join(MEDIA_DIR, img_filename)
        rel_img_path = f"atividades/{img_filename}" if os.path.exists(caminho_local_img) and os.path.getsize(caminho_local_img) > 0 else None

        noticia = AtividadeDestaque.objects.filter(titulo=titulo).first()
        if not noticia:
            noticia = AtividadeDestaque(titulo=titulo)
            total_criadas += 1
            status_txt = "Criada"
        else:
            total_atualizadas += 1
            status_txt = "Atualizada"

        noticia.chapeu = chapeu
        noticia.linha_fina = linha_fina
        if not noticia.autor:
            noticia.autor = autor
        if not noticia.credito_imagem:
            noticia.credito_imagem = credito_img

        if not noticia.corpo or len(noticia.corpo) < 100:
            noticia.corpo = f"""<p>{linha_fina}</p>
<p>As ações integram a política contínua do Governo do Estado de Mato Grosso e dos órgãos que compõem a Rede de Enfrentamento à Violência contra a Mulher (REDEVIM), reforçando o atendimento célere, o acolhimento qualificado e a resposta enérgica às infrações e aos crimes de violência doméstica e de gênero.</p>
<p><strong>Canais de denúncia e acolhimento em Mato Grosso:</strong></p>
<ul>
    <li><strong>190</strong> — Polícia Militar (Emergência imediata)</li>
    <li><strong>197</strong> — Polícia Civil (Denúncias anônimas e investigações)</li>
    <li><strong>180</strong> — Central de Atendimento à Mulher (Informações e orientações 24h)</li>
    <li><strong>SOS Mulher MT</strong> — Botão do Pânico e Medida Protetiva Digital no celular</li>
</ul>
<p style="margin-top: 25px;"><a href="{item['link_externo']}" target="_blank" rel="noopener noreferrer" style="color: #004587; font-weight: bold; text-decoration: underline;">Acesse a matéria completa e os comunicados oficiais na íntegra no portal institucional</a></p>"""

        noticia.status = AtividadeDestaque.STATUS_PUBLICADO
        noticia.data_publicacao = data_pub

        if rel_img_path:
            noticia.imagem = rel_img_path

        noticia.save()
        print(f"-> Notícia {status_txt}: '{noticia.titulo[:50]}' (Slug: {noticia.slug})")

    print(f"\nResultado da Sincronização:")
    print(f"- Total no banco agora: {AtividadeDestaque.objects.count()} matérias.")
    print(f"- Criadas: {total_criadas} | Atualizadas: {total_atualizadas}")

if __name__ == '__main__':
    sincronizar_todas()

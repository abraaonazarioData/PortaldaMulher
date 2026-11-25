import os
import django
import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_django.settings')
django.setup()

from core.models import PageContent, EmpresaCertificadaSelo

API_URL = "https://simplifica-dev.mt.gov.br/api/1/procon-publico/seloNaoENaoProcon/Selo/listarSelosPublicosVigentes"

def sincronizar_selos():
    servico = PageContent.objects.filter(slug='selo-empresa-amiga-da-mulher').first()
    if not servico:
        servico = PageContent.objects.filter(title__icontains='Selo Empresa Amiga').first()
    
    print(f"[*] Vinculando registros ao serviço: {servico}")
    print(f"[*] Consultando API: {API_URL}")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    }

    try:
        resp = requests.get(API_URL, headers=headers, verify=False, timeout=20)
        resp.raise_for_status()
        items = resp.json()
    except Exception as e:
        print(f"[!] Erro ao conectar na API: {e}")
        return

    print(f"[*] Total de itens retornados pela API: {len(items)}")

    criados = 0
    atualizados = 0

    for item in items:
        # Mapeamento flexível dos campos retornados pela API do Procon
        nome = item.get('razaoSocial') or item.get('nomeEmpresa') or item.get('nome') or item.get('estabelecimento') or ''
        cnpj = item.get('cnpj') or item.get('documento') or ''
        municipio = item.get('municipio') or item.get('cidade') or 'Cuiabá / Mato Grosso'
        endereco = item.get('endereco') or item.get('logradouro') or ''
        numero = item.get('numero') or ''
        bairro = item.get('bairro') or ''
        if numero and numero not in endereco:
            endereco = f"{endereco}, {numero}".strip(', ')
        if bairro and bairro not in endereco:
            endereco = f"{endereco} - {bairro}".strip(' -')

        instagram = item.get('instagram') or item.get('redeSocial') or ''
        
        # Validade
        val_str = item.get('dataValidade') or item.get('validade') or item.get('dataFim') or ''
        validade = None
        if val_str:
            for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S'):
                try:
                    validade = datetime.strptime(val_str[:10], fmt[:8] if 'T' in val_str else fmt).date()
                    break
                except Exception:
                    pass

        # Coordenadas
        lat = item.get('latitude') or item.get('lat')
        lng = item.get('longitude') or item.get('lng') or item.get('long')
        try:
            latitude = float(lat) if lat is not None else None
            longitude = float(lng) if lng is not None else None
        except Exception:
            latitude, longitude = None, None

        status = 'Vigente'
        if item.get('status'):
            st_raw = str(item.get('status')).capitalize()
            if 'Expir' in st_raw:
                status = 'Expirado'
            elif 'Susp' in st_raw:
                status = 'Suspenso'

        if not nome and not cnpj:
            continue

        empresa, created = EmpresaCertificadaSelo.objects.update_or_create(
            cnpj=cnpj,
            nome=nome,
            defaults={
                'servico': servico,
                'municipio': municipio,
                'endereco': endereco,
                'instagram': instagram,
                'validade': validade,
                'status': status,
                'latitude': latitude,
                'longitude': longitude,
            }
        )
        if created:
            criados += 1
        else:
            atualizados += 1

    print(f"[OK] Sincronização concluída! {criados} novas empresas criadas, {atualizados} atualizadas.")

if __name__ == '__main__':
    sincronizar_selos()

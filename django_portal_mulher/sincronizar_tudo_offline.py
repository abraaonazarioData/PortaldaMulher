import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_django.settings')

import django
django.setup()

from core.models import PageContent, Tema, AtividadeDestaque

print("1. Sincronizando Painel e Dados (PowerBI)...")
tema_paineis, _ = Tema.objects.get_or_create(
    slug='paineis-e-dados',
    defaults={'nome': 'Painéis e Dados', 'ordem': 5}
)

# Painel 1
p1, created = PageContent.objects.update_or_create(
    slug="monitoramento-da-violencia",
    defaults={
        "tema": tema_paineis,
        "title": "Monitoramento da Violência",
        "text": '<p style="text-align:justify">O Painel de Monitoramento da Violência contra a Mulher em Mato Grosso reúne dados sobre feminicídios, homicídios de mulheres e outros casos de violência no estado. As informações ajudam a acompanhar os registros e a planejar ações de prevenção e combate à violência contra a mulher.</p>',
        "link_url": "https://app.powerbi.com/view?r=eyJrIjoiNTVmNTQ4MDItMjYxMy00MmEyLTllMDktNmRkNjk5NDBmZDljIiwidCI6IjY1OWNlMmI4LTA3MTQtNDE5OC04YzM4LWRjOWI2MGFhYmI1NyJ9"
    }
)
print(f"  [OK] Monitoramento da Violência: ID={p1.id}")

# Painel 2
p2, created = PageContent.objects.update_or_create(
    slug="politicas-implementadas",
    defaults={
        "tema": tema_paineis,
        "title": "Políticas Implementadas",
        "text": '<p>Painel que apresenta as políticas públicas e ações do Governo de Mato Grosso voltadas às mulheres, incluindo iniciativas de combate à violência, acesso à justiça, segurança, educação e comunicação. Permite conhecer e acompanhar as ações realizadas para garantir os direitos e a proteção das mulheres.</p>',
        "link_url": "https://app.powerbi.com/view?r=eyJrIjoiNTFlNWNlMWEtMjllNy00N2E5LTk1OGItYzA2ZGJjZTFhZTUzIiwidCI6IjIxODk0ZWU5LWI1NzctNDNjYS04ZmY1LTQ5YjIzYzVhZDM3NSJ9"
    }
)
print(f"  [OK] Políticas Implementadas: ID={p2.id}")

print("\n2. Sincronizando Serviços e Políticas Públicas...")
tema_servicos, _ = Tema.objects.get_or_create(
    slug='servicos-e-politicas-publicas',
    defaults={'nome': 'Serviços e Políticas Públicas', 'ordem': 2}
)

s1, _ = PageContent.objects.update_or_create(
    slug="abrir-ocorrencias",
    defaults={
        "tema": tema_servicos,
        "title": "Abrir ocorrências",
        "text": "Link direto para registro de ocorrência online e pedido de medida protetiva pela internet.",
        "link_url": "https://delegaciadigital.pjc.mt.gov.br/"
    }
)
s2, _ = PageContent.objects.update_or_create(
    slug="meninas-que-transformam",
    defaults={
        "tema": tema_servicos,
        "title": "Meninas que Transformam",
        "text": "Programa para apoiar o desenvolvimento, a autonomia e a preparação de jovens e adolescentes para o mercado de trabalho.",
        "link_url": "https://seletivo.seplag.mt.gov.br/detalhes/53?slug=pss-programa-meninas-que-transformam-2026"
    }
)
s3, _ = PageContent.objects.update_or_create(
    slug="patrulha-maria-da-penha",
    defaults={
        "tema": tema_servicos,
        "title": "Patrulha Maria da Penha",
        "text": "Garantir a segurança da mulher e eficácia das medidas protetivas de urgência que o agressor deve cumprir.",
        "link_url": "https://www.pm.mt.gov.br/pmp"
    }
)
print(f"  [OK] Serviços configurados com links clicáveis!")

print(f"\n3. Total de Notícias no banco (AtividadeDestaque): {AtividadeDestaque.objects.count()}")
print("Sincronização offline concluída com 100% de sucesso!")

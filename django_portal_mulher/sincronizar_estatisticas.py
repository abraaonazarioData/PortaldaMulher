import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_django.settings')

import django
django.setup()

from core.models import PageContent, Tema

tema, created = Tema.objects.get_or_create(
    slug='paineis-e-dados',
    defaults={'nome': 'Painéis e Dados', 'ordem': 5}
)

print(f"Tema: {tema.nome} (ID: {tema.id})")

# Remover itens de teste cadastrados localmente (teste, teste04, globo.com, etc)
antigos = PageContent.objects.filter(tema=tema)
for item in antigos:
    print(f"Removendo/Resetando item anterior: ID={item.id} | Titulo='{item.title}'")
    item.delete()

# Criar Painel 1 oficial de Produção
p1 = PageContent.objects.create(
    tema=tema,
    title="Monitoramento da Violência",
    slug="monitoramento-da-violencia",
    text='<p style="text-align:justify">O Painel de Monitoramento da Violência contra a Mulher em Mato Grosso reúne dados sobre feminicídios, homicídios de mulheres e outros casos de violência no estado. As informações ajudam a acompanhar os registros e a planejar ações de prevenção e combate à violência contra a mulher.</p>',
    link_url="https://app.powerbi.com/view?r=eyJrIjoiNTVmNTQ4MDItMjYxMy00MmEyLTllMDktNmRkNjk5NDBmZDljIiwidCI6IjY1OWNlMmI4LTA3MTQtNDE5OC04YzM4LWRjOWI2MGFhYmI1NyJ9"
)
print(f"[OK] Painel 1 criado com sucesso: ID={p1.id} | '{p1.title}'")

# Criar Painel 2 oficial de Produção
p2 = PageContent.objects.create(
    tema=tema,
    title="Políticas Implementadas",
    slug="politicas-implementadas",
    text='<p>Painel que apresenta as políticas públicas e ações do Governo de Mato Grosso voltadas às mulheres, incluindo iniciativas de combate à violência, acesso à justiça, segurança, educação e comunicação. Permite conhecer e acompanhar as ações realizadas para garantir os direitos e a proteção das mulheres.</p>',
    link_url="https://app.powerbi.com/view?r=eyJrIjoiNTFlNWNlMWEtMjllNy00N2E5LTk1OGItYzA2ZGJjZTFhZTUzIiwidCI6IjIxODk0ZWU5LWI1NzctNDNjYS04ZmY1LTQ5YjIzYzVhZDM3NSJ9"
)
print(f"[OK] Painel 2 criado com sucesso: ID={p2.id} | '{p2.title}'")

print(f"\nTotal de painéis agora no banco: {PageContent.objects.filter(tema=tema).count()}")

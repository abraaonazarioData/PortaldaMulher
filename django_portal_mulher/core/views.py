from django.shortcuts import render
from django.http import JsonResponse
import unicodedata
from .models import RedeProtecao, PageContent, BannerInicial, AtividadeDestaque, ParceiroInstitucional, Ouvidoria
import json
def home(request):
    # Busca a rede de proteção no banco de dados (SQLite)
    redes = list(RedeProtecao.objects.values())
    
    # Busca os vídeos/materiais cadastrados no Painel do Django, filtrando pelo Tema
    materiais = PageContent.objects.filter(tema__slug='materiais-educativos').order_by('id')
    servicos = PageContent.objects.filter(tema__slug='servicos-e-politicas-publicas').order_by('id')
    ajuda = PageContent.objects.filter(tema__slug='preciso-de-ajuda').order_by('id')
    paineis = PageContent.objects.filter(tema__slug='paineis-e-dados').order_by('id')
    banners = BannerInicial.objects.filter(ativo=True).order_by('ordem', '-id')
    atividades_destaque = AtividadeDestaque.objects.order_by('-data_publicacao')[:5]
    parceiros = ParceiroInstitucional.objects.all().order_by('ordem')
    planos_metas = PageContent.objects.filter(tema__slug='planos-e-metas').order_by('id')[:4]
    legislacao_destaque = PageContent.objects.filter(tema__slug='legislacao-destaque').order_by('id')[:2]
    
    # Obtém registro da Ouvidoria (proxy) e garante fallback de imagem
    ouvidoria = Ouvidoria.objects.filter(slug='ouvidoria').first()
    if not ouvidoria:
        # cria tema e registro padrão se ausente (mesmo que já exista em dashboard view)
        tema, _ = Tema.objects.get_or_create(slug='ouvidoria', defaults={'nome': 'Ouvidoria', 'ordem': 0})
        ouvidoria = PageContent.objects.create(
            tema=tema,
            title='Ouvidoria',
            slug='ouvidoria',
            text='Acesse o canal da Ouvidoria para registrar manifestações, sugestões ou reclamações.',
            link_url='https://ouvidoria.cge.mt.gov.br',
        )
    # URL segura da imagem para template
    ouvidoria_image_url = ouvidoria.image.url if ouvidoria.image else 'https://ouvidoria.cge.mt.gov.br/_next/static/media/CGE%20-%20Fale%20Cidad%C3%A3o%20v1.da578e70.svg'


    # Contador de visitas
    from .models import VisitCounter
    counter, created = VisitCounter.objects.get_or_create(id=1)
    
    # Incrementa apenas se for uma nova sessão (opcional) ou sempre que acessar a home
    if not request.session.get('has_visited', False):
        counter.count += 1
        counter.save()
        request.session['has_visited'] = True

    context = {
        'ouvidoria_image_url': ouvidoria_image_url,
        'redes_json': json.dumps(redes),
        'materiais': materiais,
        'servicos': servicos,
        'ajuda': ajuda,
        'paineis': paineis,
        'visit_count': counter.count,
        'banners': banners,
        'atividades_destaque': atividades_destaque,
        'parceiros': parceiros,
        'planos_metas': planos_metas,
        'legislacao_destaque': legislacao_destaque,
        'ouvidoria': ouvidoria,
    }
    return render(request, 'index.html', context)

def servicos(request):
    return render(request, "servicos.html")

def legislacao(request):
    legislacoes = PageContent.objects.filter(tema__slug='legislacao').order_by('id')
    return render(request, "legislacao.html", {"legislacoes": legislacoes})

def atendimentos(request):
    redes = list(RedeProtecao.objects.values())
    return render(request, "atendimentos.html", {"redes_json": json.dumps(redes)})

def ocorrencias(request):
    return render(request, "ocorrencias.html")

def acessibilidade(request):
    return render(request, "acessibilidade.html")

def planos_metas(request):
    planos = PageContent.objects.filter(tema__slug='planos-e-metas').order_by('id')
    return render(request, "planos_metas.html", {"planos": planos})

def estatisticas(request):
    paineis = PageContent.objects.filter(tema__slug='paineis-e-dados').order_by('id')
    return render(request, "Estatisticas.html", {"paineis": paineis})

def atividades(request):
    todas_atividades = AtividadeDestaque.objects.all().order_by('-data_publicacao')
    return render(request, "atividades.html", {"atividades": todas_atividades})

def noticia_detalhe(request, id):
    from django.shortcuts import get_object_or_404
    noticia = get_object_or_404(AtividadeDestaque, id=id)
    return render(request, "noticia_detalhe.html", {"noticia": noticia})

def modulo1(request):
    return render(request, "modulo1_gabinete.html")

def modulo2(request):
    return render(request, "modulo2_monitoramento.html")

def modulo3(request):
    return render(request, "modulo3_metas.html")

def modulo4(request):
    redes = list(RedeProtecao.objects.values())
    return render(request, "modulo4_mapa_rede.html", {"redes_json": json.dumps(redes)})

def documentos(request):
    todas_legislacoes = PageContent.objects.filter(tema__slug='legislacao').order_by('id')
    
    leis_federais = []
    leis_estaduais = []
    decretos = []
    outros = []
    
    for leg in todas_legislacoes:
        t = leg.title.lower()
        txt = leg.text.lower()
        if 'decreto' in t or 'normativa' in t or 'portaria' in t or 'resolução' in t:
            decretos.append(leg)
        elif 'federal' in t or 'nacional' in t or 'união' in t:
            leis_federais.append(leg)
        elif 'estadual' in t or 'mato grosso' in t or ' mt' in t or 'mt ' in t:
            leis_estaduais.append(leg)
        else:
            # Se não conseguir identificar automaticamente, coloca em 'Pendente' / Outros
            outros.append(leg)

    relatorios = PageContent.objects.filter(tema__slug='relatorios').order_by('id')
    estudos = PageContent.objects.filter(tema__slug='estudos').order_by('id')
    return render(request, "documentos.html", {
        "leis_federais": leis_federais,
        "leis_estaduais": leis_estaduais,
        "decretos": decretos,
        "outras_legislacoes": outros,
        "relatorios": relatorios,
        "estudos": estudos
    })

def conheca(request):
    conteudo_rede = PageContent.objects.filter(tema__slug='sobre-o-portal').first()
    return render(request, "conheca.html", {"conteudo_rede": conteudo_rede})

def modulo5(request):
    return render(request, "modulo5_diagnotico.html")

def modulo6(request):
    return render(request, "modulo6_educativos.html")

def modulo7(request):
    return render(request, "modulo7_integracao.html")

def modulo8(request):
    return render(request, "modulo8_orcamento.html")

def politica_privacidade(request):
    return render(request, "politica_privacidade.html")

def mapa_site(request):
    return render(request, "mapa_site.html")

def fonar(request):
    return render(request, "diagnostico_fonar.html")


def fale_cidadao(request):
    return render(request, 'fale_cidadao.html')

def bi_interativo(request):
    from .models import EstatisticaViolencia
    # Pass all stats as JSON so frontend can filter interactively
    stats = list(EstatisticaViolencia.objects.values(
        'municipio', 'tipo_crime', 'ano', 'mes', 'quantidade', 'perfil_vitima_idade', 'perfil_vitima_raca'
    ))
    return render(request, "bi_interativo.html", {"stats_json": json.dumps(stats)})

def chat_api(request):
    if request.method == "GET":
        user_message = request.GET.get("message", "")
    else:
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
        except:
            user_message = ""

    if not user_message:
        return JsonResponse({"response": "Por favor, digite uma mensagem."}, status=400)

    def normalizar(texto):
        texto = texto.lower()
        texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
        return texto

    msg_norm = normalizar(user_message)

    # 1. Emergência
    palavras_emergencia = ['socorro', 'ajuda', 'bater', 'batendo', 'agressao', 'agredida', 'denunciar', 'denuncia', 'medo', 'matar']
    if any(p in msg_norm for p in palavras_emergencia):
        resposta = (
            "🚨 **Você não está sozinha!**\n\n"
            "Se você ou alguém estiver em perigo agora, ligue IMEDIATAMENTE para a **Polícia Militar (190)** "
            "ou para a **Central da Mulher (180)**.\n\n"
            "Vá para um local seguro. A ajuda vai chegar rápido."
        )
        return JsonResponse({"response": resposta})

    # 2. Busca por Serviços
    tipos_map = {
        'delegacia': 'DEDM',
        'unidade especializada': 'DEDM',
        'dedm': 'DEDM',
        'núcleo': 'NUCLEO',
        'nucleo': 'NUCLEO',
        'patrulha': 'PMP'
    }

    tipo_buscado = None
    for palavra, tipo in tipos_map.items():
        if palavra in msg_norm:
            tipo_buscado = tipo
            break

    cidades_base = list(set(normalizar(item['cidade']) for item in RedeProtecao.objects.values('cidade')))
    cidade_buscada = None
    for cidade in cidades_base:
        if cidade in msg_norm:
            cidade_buscada = cidade
            break

    if tipo_buscado or cidade_buscada:
        query = RedeProtecao.objects.all()
        if tipo_buscado:
            query = query.filter(tipo=tipo_buscado)
        
        resultados = []
        for item in query:
            if cidade_buscada and normalizar(item.cidade) != cidade_buscada:
                continue
            resultados.append(f"📍 **{item.nome}**\n  Endereço: {item.endereco}\n  Telefone: {item.telefone}")
            
        if resultados:
            resposta = "Encontrei estes locais de atendimento para você:\n\n" + "\n\n".join(resultados) + "\n\nSe precisar de mais algo, me avise!"
        else:
            resposta = "Não encontrei esse local na nossa base. Mas lembre-se: você pode ligar **180** de qualquer telefone para pedir ajuda ou tirar dúvidas de graça."
        return JsonResponse({"response": resposta})

    # 3.5 Rede de Apoio
    palavras_rede = ['rede de apoio', 'rede de protecao', 'quem faz parte', 'orgaos', 'órgãos', 'plano de metas', 'decreto', '1708']
    if any(p in msg_norm for p in palavras_rede):
        resposta = (
            "O Estado de MT possui uma forte **Rede de Proteção** para te ajudar (Plano de Metas).\n\n"
            "**Quem faz parte:**\n"
            "- Polícias, Bombeiros e POLITEC.\n"
            "- Gabinete da Mulher e Secretarias do Governo.\n"
            "- Parceiros da Justiça (Tribunais, Defensoria, Ministério Público e OAB).\n\n"
            "Nosso objetivo é educar, proteger e garantir seus direitos de forma rápida."
        )
        return JsonResponse({"response": resposta})

    # 3.6 Politicas
    palavras_politicas = ['politicas publicas', 'politicas', 'servicos', 'programas']
    if any(p in msg_norm for p in palavras_politicas):
        return JsonResponse({"response": "No Portal, você encontra informações sobre Políticas Públicas voltadas para a mulher, como programas de autonomia financeira, capacitação e acolhimento."})

    # 3.9 Maria da Penha
    if 'maria da penha' in msg_norm or '11.340' in msg_norm:
        return JsonResponse({"response": "A **Lei Maria da Penha (Lei 11.340/2006)** é a principal lei brasileira para coibir a violência doméstica e familiar contra a mulher. Ela prevê medidas protetivas de urgência, criação de juizados especiais e endurecimento das penas. No nosso portal, na seção de Legislação e Materiais Educativos, você encontra cartilhas explicando a lei em detalhes."})

    # 3.10 Leis
    if any(p in msg_norm for p in ['lei', 'leis', 'legislacao', 'direitos']):
        return JsonResponse({"response": "Na seção de Legislação do Portal você encontra informações sobre a Lei Maria da Penha, o Estatuto da Mulher, a Lei da Violência Doméstica e outras normas que protegem as mulheres. Consulte nossos materiais educativos para mais detalhes."})

    # 3.7 Materiais
    palavras_edu = ['materiais', 'educativos', 'cartilhas', 'livros', 'aprender']
    if any(p in msg_norm for p in palavras_edu):
        return JsonResponse({"response": "Oferecemos diversos Materiais Educativos (cartilhas, guias e vídeos) para conscientização sobre os direitos das mulheres e combate à violência."})

    # 3.8 Portal
    if 'sobre' in msg_norm and 'portal' in msg_norm:
        return JsonResponse({"response": "Este é o Portal Oficial de Defesa das Mulheres do Governo de MT. Aqui centralizamos acesso a serviços, rede de proteção, denúncias e materiais educativos."})

    # 4. Fallback
    resposta = (
        "Desculpe, não consegui entender completamente. \n\n"
        "Você pode tentar me perguntar sobre:\n"
        "- **Locais de atendimento** (ex: 'delegacia em Sinop')\n"
        "- **Pedido de ajuda** (ex: 'preciso de ajuda')\n"
        "- **Leis e Direitos** (ex: 'maria da penha')\n\n"
        "Se for uma emergência, ligue 190 ou 180."
    )
    return JsonResponse({"response": resposta})

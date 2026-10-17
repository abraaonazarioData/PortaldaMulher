from django.shortcuts import render
from django.http import JsonResponse
import unicodedata
from .models import RedeProtecao, PageContent, BannerInicial, AtividadeDestaque, ParceiroInstitucional, Ouvidoria, Tema
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
    atividades_destaque = AtividadeDestaque.objects.publicadas().order_by('-data_publicacao')[:5]
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


    # Contador de visitas (atômico contra concorrência)
    from .models import VisitCounter
    from django.db.models import F
    counter, created = VisitCounter.objects.get_or_create(id=1)
    
    # Incrementa apenas se for uma nova sessão
    if not request.session.get('has_visited', False):
        VisitCounter.objects.filter(id=1).update(count=F('count') + 1)
        counter.refresh_from_db()
        request.session['has_visited'] = True

    context = {
        'ouvidoria_image_url': ouvidoria_image_url,
        'redes': redes,
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
    return render(request, "atendimentos.html", {"redes": redes, "redes_json": json.dumps(redes)})

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
    from django.core.paginator import Paginator
    qs = AtividadeDestaque.objects.publicadas().order_by('-data_publicacao')
    pagina = Paginator(qs, 10).get_page(request.GET.get('page'))
    return render(request, "atividades.html", {"atividades": pagina, "page_obj": pagina})

def noticia_detalhe(request, slug):
    from django.shortcuts import get_object_or_404
    noticia = get_object_or_404(AtividadeDestaque.objects.publicadas(), slug=slug)
    return render(request, "noticia_detalhe.html", {"noticia": noticia})

def noticia_por_id(request, id):
    """Compatibilidade com links antigos /noticia/<id>/ -> /noticias/<slug>/"""
    from django.shortcuts import get_object_or_404, redirect
    noticia = get_object_or_404(AtividadeDestaque.objects.publicadas(), id=id)
    return redirect(noticia, permanent=True)

def noticia_previa(request, pk):
    """Pré-visualização (inclusive rascunhos) – apenas equipe autenticada."""
    from django.shortcuts import get_object_or_404
    from django.http import Http404
    from django.urls import reverse
    if not (request.user.is_authenticated and request.user.is_staff):
        raise Http404
    noticia = get_object_or_404(AtividadeDestaque, pk=pk)
    return render(request, "noticia_detalhe.html", {
        "noticia": noticia,
        "previa": True,
        "url_edicao": reverse('admin:core_atividadedestaque_change', args=[pk]),
    })

def modulo1(request):
    return render(request, "modulo1_gabinete.html")

def modulo2(request):
    return render(request, "modulo2_monitoramento.html")

def modulo3(request):
    return render(request, "modulo3_metas.html")

def modulo4(request):
    redes = list(RedeProtecao.objects.values())
    return render(request, "modulo4_mapa_rede.html", {"redes": redes, "redes_json": json.dumps(redes)})

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
    # Pass all stats as dicts so frontend can use json_script safely
    stats = list(EstatisticaViolencia.objects.values(
        'municipio', 'tipo_crime', 'ano', 'mes', 'quantidade', 'perfil_vitima_idade', 'perfil_vitima_raca'
    ))
    return render(request, "bi_interativo.html", {"stats": stats, "stats_json": json.dumps(stats)})

def chat_api(request):
    import re
    from django.core.cache import cache

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")
        except (json.JSONDecodeError, ValueError, AttributeError):
            user_message = ""
    else:
        user_message = request.GET.get("message", "")

    user_message = str(user_message).strip()
    if not user_message:
        return JsonResponse({"response": "Por favor, digite uma mensagem."}, status=400)

    # Limitar tamanho máximo para prevenir abuso / DoS
    if len(user_message) > 500:
        user_message = user_message[:500]

    def normalizar(texto):
        texto = texto.lower()
        texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
        return texto

    msg_norm = normalizar(user_message)

    # 1. Emergência (palavras inteiras via regex \b)
    palavras_emergencia = [
        r'\bsocorro\b', r'\bajuda\b', r'\bbater\b', r'\bbatendo\b',
        r'\bagressao\b', r'\bagredida\b', r'\bdenunciar\b', r'\bdenuncia\b',
        r'\bmedo\b', r'\bmatar\b', r'\bameaca\b'
    ]
    if any(re.search(p, msg_norm) for p in palavras_emergencia):
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
        'nucleo': 'NUCLEO',
        'patrulha': 'PMP'
    }

    tipo_buscado = None
    for palavra, tipo in tipos_map.items():
        if re.search(r'\b' + re.escape(palavra) + r'\b', msg_norm):
            tipo_buscado = tipo
            break

    # Cache de cidades da rede por 1 hora
    def get_cidades():
        return list(set(normalizar(c) for c in RedeProtecao.objects.values_list('cidade', flat=True) if c))
    
    cidades_base = cache.get_or_set('chat_cidades_rede', get_cidades, 3600)
    cidade_buscada = None
    for cidade in cidades_base:
        if re.search(r'\b' + re.escape(cidade) + r'\b', msg_norm):
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
            if len(resultados) >= 8:
                break
            
        if resultados:
            resposta = "Encontrei estes locais de atendimento para você:\n\n" + "\n\n".join(resultados) + "\n\nSe precisar de mais algo, me avise!"
        else:
            resposta = "Não encontrei esse local na nossa base. Mas lembre-se: você pode ligar **180** de qualquer telefone para pedir ajuda ou tirar dúvidas de graça."
        return JsonResponse({"response": resposta})

    # 3. Rede de Apoio
    if re.search(r'\b(rede de apoio|rede de protecao|quem faz parte|orgaos|plano de metas|decreto 1708|1708)\b', msg_norm):
        resposta = (
            "O Estado de MT possui uma forte **Rede de Proteção** para te ajudar (Plano de Metas).\n\n"
            "**Quem faz parte:**\n"
            "- Polícias, Bombeiros e POLITEC.\n"
            "- Gabinete da Mulher e Secretarias do Governo.\n"
            "- Parceiros da Justiça (Tribunais, Defensoria, Ministério Público e OAB).\n\n"
            "Nosso objetivo é educar, proteger e garantir seus direitos de forma rápida."
        )
        return JsonResponse({"response": resposta})

    # 4. Políticas Públicas
    if re.search(r'\b(politicas publicas|politicas|programas)\b', msg_norm):
        return JsonResponse({"response": "No Portal, você encontra informações sobre Políticas Públicas voltadas para a mulher, como programas de autonomia financeira, capacitação e acolhimento."})

    # 5. Maria da Penha
    if re.search(r'\b(maria da penha|11\.340|11340)\b', msg_norm):
        return JsonResponse({"response": "A **Lei Maria da Penha (Lei 11.340/2006)** é a principal lei brasileira para coibir a violência doméstica e familiar contra a mulher. Ela prevê medidas protetivas de urgência, criação de juizados especiais e endurecimento das penas. No nosso portal, na seção de Legislação e Materiais Educativos, você encontra cartilhas explicando a lei em detalhes."})

    # 6. Leis
    if re.search(r'\b(lei|leis|legislacao|direitos)\b', msg_norm):
        return JsonResponse({"response": "Na seção de Legislação do Portal você encontra informações sobre a Lei Maria da Penha, o Estatuto da Mulher, a Lei da Violência Doméstica e outras normas que protegem as mulheres. Consulte nossos materiais educativos para mais detalhes."})

    # 7. Materiais Educativos
    if re.search(r'\b(materiais|cartilhas|livros|aprender|cartilha)\b', msg_norm):
        return JsonResponse({"response": "Oferecemos diversos Materiais Educativos (cartilhas, guias e vídeos) para conscientização sobre os direitos das mulheres e combate à violência."})

    # 8. Sobre o Portal
    if re.search(r'\b(sobre o portal|o que e o portal|portal mulher)\b', msg_norm) or ('sobre' in msg_norm and 'portal' in msg_norm):
        return JsonResponse({"response": "Este é o Portal Oficial de Defesa das Mulheres do Governo de MT. Aqui centralizamos acesso a serviços, rede de proteção, denúncias e materiais educativos."})

    # 9. Fallback
    resposta = (
        "Desculpe, não consegui entender completamente. \n\n"
        "Você pode tentar me perguntar sobre:\n"
        "- **Locais de atendimento** (ex: 'delegacia em Sinop')\n"
        "- **Pedido de ajuda** (ex: 'preciso de ajuda')\n"
        "- **Leis e Direitos** (ex: 'maria da penha')\n\n"
        "Se for uma emergência, ligue 190 ou 180."
    )
    return JsonResponse({"response": resposta})


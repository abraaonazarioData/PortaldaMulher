from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import PageContent, RedeProtecao, Tema, Ouvidoria
from django.contrib.auth.models import User

def is_staff(user):
    return user.is_staff

@login_required(login_url='/SysteGEVM9x2/login/')
@user_passes_test(is_staff, login_url='/SysteGEVM9x2/login/')
def dashboard_home(request):
    from .models import PanelVisitCounter
    from django.db.models import F
    counter, _ = PanelVisitCounter.objects.get_or_create(id=1)
    
    if not request.session.get('has_visited_panel', False):
        PanelVisitCounter.objects.filter(id=1).update(count=F('count') + 1)
        counter.refresh_from_db()
        request.session['has_visited_panel'] = True

    # Garantir que exista um registro de Ouvidoria
    ouvidoria = Ouvidoria.objects.filter(slug='ouvidoria').first()
    if not ouvidoria:
        # Cria o Tema "ouvidoria" se não existir
        tema, _ = Tema.objects.get_or_create(slug='ouvidoria', defaults={'nome': 'Ouvidoria', 'ordem': 0})
        # Cria o conteúdo da Ouvidoria
        ouvidoria = PageContent.objects.create(
            tema=tema,
            title='Ouvidoria',
            slug='ouvidoria',
            text='Acesse o canal da Ouvidoria para registrar manifestações, sugestões ou reclamações.',
            link_url='https://ouvidoria.cge.mt.gov.br',
        )
    # URL segura da imagem para template
    ouvidoria_image_url = ouvidoria.image.url if ouvidoria.image else 'https://ouvidoria.cge.mt.gov.br/_next/static/media/CGE%20-%20Fale%20Cidad%C3%A3o%20v1.da578e70.svg'
    context = {
        'total_conteudos': PageContent.objects.count(),
        'total_redes': RedeProtecao.objects.count(),
        'total_temas': Tema.objects.count(),
        'total_usuarios': User.objects.count(),
        'total_acessos_painel': counter.count,
        'ouvidoria': ouvidoria,
        'ouvidoria_image_url': ouvidoria_image_url,
    }

    return render(request, 'dashboard/home.html', context)

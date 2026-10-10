from django import template
from core.models import PageContent, RedeProtecao, Tema, PanelVisitCounter
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def get_dashboard_stats():
    counter, created = PanelVisitCounter.objects.get_or_create(id=1)
    counter.count += 1
    counter.save()
    
    return {
        'total_conteudos': PageContent.objects.count(),
        'total_redes': RedeProtecao.objects.count(),
        'total_temas': Tema.objects.count(),
        'total_usuarios': User.objects.count(),
        'acessos_painel': counter.count,
    }

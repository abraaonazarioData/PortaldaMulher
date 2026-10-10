from django.shortcuts import render

class BlockDebug404Middleware:
    """
    Este middleware intercepta respostas 404 (Não Encontrado)
    e força a exibição da nossa página 404 customizada, mesmo quando
    o DEBUG está ativado (True). Isso impede o vazamento da lista
    de URLs secretas (como a URL do painel Admin).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Se a página não foi encontrada (404), mostra o nosso template seguro
        if response.status_code == 404:
            return render(request, '404.html', status=404)
            
        return response

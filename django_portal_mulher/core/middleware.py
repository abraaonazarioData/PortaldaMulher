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


class SecurityHeadersMiddleware:
    """
    Middleware que reforça cabeçalhos de segurança essenciais:
    - Content-Security-Policy (CSP)
    - Strict-Transport-Security (HSTS)
    - Referrer-Policy
    - Permissions-Policy
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # HSTS (Strict-Transport-Security) se conexão segura ou via proxy HTTPS
        is_ssl = (
            request.is_secure() or
            request.headers.get('X-Forwarded-Proto', '').lower() == 'https' or
            request.META.get('HTTP_X_FORWARDED_PROTO', '').lower() == 'https'
        )
        if is_ssl:
            response.headers.setdefault(
                'Strict-Transport-Security',
                'max-age=31536000; includeSubDomains; preload'
            )

        # Proteção contra vazamento de referenciador
        response.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')

        # Bloqueio de APIs invasivas do dispositivo
        response.headers.setdefault(
            'Permissions-Policy',
            'camera=(), microphone=(), geolocation=(self)'
        )

        # Content-Security-Policy (CSP) compatível com o portal
        csp_rules = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com https://cdnjs.cloudflare.com",
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://unpkg.com https://cdnjs.cloudflare.com",
            "font-src 'self' data: https://fonts.gstatic.com https://cdnjs.cloudflare.com",
            "img-src 'self' data: https: http: blob:",
            "connect-src 'self' https://mulher.mt.gov.br",
            "frame-src 'self' https://www.youtube.com https://youtube.com https://ouvidoria.cge.mt.gov.br",
            "base-uri 'self'",
            "form-action 'self'",
        ]
        response.headers.setdefault('Content-Security-Policy', "; ".join(csp_rules))

        return response


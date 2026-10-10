from django.urls import path, URLPattern, URLResolver, get_resolver
from django.http import HttpResponse

# Recursive collector of URL patterns
def _collect_urls(patterns, prefix=''):
    collected = []
    for p in patterns:
        if isinstance(p, URLPattern):
            collected.append({
                'pattern': prefix + str(p.pattern),
                'callback': f"{p.callback.__module__}.{p.callback.__name__}",
                'name': p.name or ''
            })
        elif isinstance(p, URLResolver):
            collected.extend(_collect_urls(p.url_patterns, prefix + str(p.pattern)))
    return collected

def list_all_urls(request):
    urls = _collect_urls(get_resolver().url_patterns)
    rows = ''.join(
        f"<tr><td>{u['pattern']}</td><td>{u['callback']}</td><td>{u['name']}</td></tr>"
        for u in urls
    )
    html = f"""
    <h2>All URL Patterns</h2>
    <table border='1' cellpadding='5' cellspacing='0'>
        <thead><tr><th>Pattern</th><th>View</th><th>Name</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>
    """
    return HttpResponse(html)

# URL for admin
from django.contrib import admin
admin_extra_urls = [
    path('all-urls/', admin.site.admin_view(list_all_urls), name='all_urls'),
]

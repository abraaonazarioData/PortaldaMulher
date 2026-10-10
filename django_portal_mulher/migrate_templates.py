import os
import re

template_dir = 'templates'

static_regex = re.compile(r"\{\{\s*url_for\s*\(\s*['\"]static['\"]\s*,\s*filename\s*=\s*(['\"][^'\"]+['\"])\s*\)\s*\}\}")
url_regex = re.compile(r"\{\{\s*url_for\s*\(\s*(['\"][^'\"]+['\"])\s*\)\s*\}\}")

for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(filepath, 'r', encoding='latin-1') as f:
                    content = f.read()
            
            needs_static = bool(static_regex.search(content))
            
            new_content = static_regex.sub(r"{% static \1 %}", content)
            new_content = url_regex.sub(r"{% url \1 %}", new_content)
            
            if needs_static and '{% load static %}' not in new_content:
                if '{% extends' in new_content:
                    new_content = re.sub(r"(\{% extends [^}]+\}%)", r"\1\n{% load static %}", new_content, count=1)
                else:
                    new_content = "{% load static %}\n" + new_content
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
print("Templates migrados com sucesso para o padrão Django.")

import os
import re

file_path = r'c:\Users\Administrator\Desktop\Portal Mulher\new\Portal Mulher\django_portal_mulher\templates\documentos.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Legislação block
leg_start = '<div class="doc-category-card" id="cat-legislacao">'
leg_end_marker = '<!-- CATEGORIA: RELATÃ“RIOS -->' # from the file: <!-- CATEGORIA: RELATÓRIOS --> wait, it's encoded weirdly.

# I will use a more robust replacement strategy using regex
import re

# 1. Replace Legislacao items
legislacao_pattern = re.compile(
    r'(<div class="doc-category-card" id="cat-legislacao">.*?<div class="doc-list">)\s*<div style="display: flex; flex-direction: column; gap: 20px;">.*?</div>\s*</div>\s*</div>',
    re.DOTALL
)
legislacao_replacement = r'''\1
    <div style="display: flex; flex-direction: column; gap: 20px;">
        {% for item in legislacoes %}
        <div style="padding: 20px; border: 1px solid #eee; border-radius: 8px; background: #f9f9f9;" class="doc-item">
            <div class="doc-item-content">
                <div style="flex: 1;">
                    <h4 style="color: #004587; margin-bottom: 10px;" class="doc-item-title">{{ item.title }}</h4>
                    <p style="color: #666; font-size: 0.95rem; margin-bottom: 15px;" class="doc-item-desc">{{ item.text }}</p>
                    {% if item.link_url %}
                    <a href="{{ item.link_url }}" target="_blank" style="color: #e91e63; font-weight: 600; text-decoration: none;" class="doc-action-btn"><i class="fa-solid fa-arrow-up-right-from-square"></i> Acessar Documento</a>
                    {% endif %}
                </div>
            </div>
        </div>
        {% empty %}
        <div class="doc-empty-state">
            <i class="fa-regular fa-folder-open"></i>
            <span>Nenhuma legislação encontrada</span>
            <p>Os documentos legislativos aparecerão aqui assim que forem cadastrados no sistema.</p>
        </div>
        {% endfor %}
    </div>
</div>
</div>'''

content = legislacao_pattern.sub(legislacao_replacement, content)


# 2. Replace Relatorios items
relatorios_pattern = re.compile(
    r'(<div class="doc-category-card" id="cat-relatorios">.*?<div class="doc-list">)\s*<div style="display: flex; flex-direction: column; gap: 20px;">.*?</div>\s*</div>\s*</div>',
    re.DOTALL
)
relatorios_replacement = r'''\1
    <div style="display: flex; flex-direction: column; gap: 20px;">
        {% for item in relatorios %}
        <div style="padding: 20px; border: 1px solid #eee; border-radius: 8px; background: #f9f9f9;" class="doc-item">
            <div class="doc-item-content">
                <div style="flex: 1;">
                    <h4 style="color: #004587; margin-bottom: 10px;" class="doc-item-title">{{ item.title }}</h4>
                    <p style="color: #666; font-size: 0.95rem; margin-bottom: 15px;" class="doc-item-desc">{{ item.text }}</p>
                    {% if item.link_url %}
                    <a href="{{ item.link_url }}" target="_blank" style="color: #e91e63; font-weight: 600; text-decoration: none;" class="doc-action-btn"><i class="fa-solid fa-arrow-up-right-from-square"></i> Acessar Documento</a>
                    {% endif %}
                </div>
            </div>
        </div>
        {% empty %}
        <div class="doc-empty-state">
            <i class="fa-regular fa-folder-open"></i>
            <span>Nenhum relatório encontrado</span>
            <p>Os relatórios oficiais aparecerão aqui assim que forem publicados no sistema.</p>
        </div>
        {% endfor %}
    </div>
</div>
</div>'''

content = relatorios_pattern.sub(relatorios_replacement, content)


# 3. Replace Estudos items
estudos_pattern = re.compile(
    r'(<div class="doc-category-card" id="cat-estudos">.*?<div class="doc-list">)\s*<div style="display: flex; flex-direction: column; gap: 20px;">.*?</div>\s*</div>\s*</div>',
    re.DOTALL
)
estudos_replacement = r'''\1
    <div style="display: flex; flex-direction: column; gap: 20px;">
        {% for item in estudos %}
        <div style="padding: 20px; border: 1px solid #eee; border-radius: 8px; background: #f9f9f9;" class="doc-item">
            <div class="doc-item-content">
                <div style="flex: 1;">
                    <h4 style="color: #004587; margin-bottom: 10px;" class="doc-item-title">{{ item.title }}</h4>
                    <p style="color: #666; font-size: 0.95rem; margin-bottom: 15px;" class="doc-item-desc">{{ item.text }}</p>
                    {% if item.link_url %}
                    <a href="{{ item.link_url }}" target="_blank" style="color: #e91e63; font-weight: 600; text-decoration: none;" class="doc-action-btn"><i class="fa-solid fa-arrow-up-right-from-square"></i> Acessar Documento</a>
                    {% endif %}
                </div>
            </div>
        </div>
        {% empty %}
        <div class="doc-empty-state doc-item">
            <i class="fa-regular fa-folder-open"></i>
            <span class="doc-item-title">Nenhum estudo publicado</span>
            <p class="doc-item-desc">Ainda não há estudos ou pesquisas cadastrados nesta seção.</p>
        </div>
        {% endfor %}
    </div>
</div>
</div>'''

content = estudos_pattern.sub(estudos_replacement, content)


with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Documentos HTML atualizado!")

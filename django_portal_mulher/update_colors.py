import re

file_path = r"c:\Users\Administrator\Desktop\Portal Mulher\new\Portal Mulher\django_portal_mulher\templates\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Preciso de Ajuda -> bg-blue theme-dark
content = content.replace(
    '<section id="preciso-ajuda" class="new-section bg-white">',
    '<section id="preciso-ajuda" class="new-section bg-blue theme-dark">'
)

# 2. Painéis e Dados -> bg-gray (já está "não azul", vou deixar bg-gray ou bg-white)
content = content.replace(
    '<section id="dados-violencia" class="new-section bg-gray"',
    '<section id="dados-violencia" class="new-section bg-white"'
)
# Fix explicit dark colors in Painéis e Dados just in case, though it's white so dark text is fine.

# 3. Atividades -> bg-blue theme-dark (Já está)

# 4. Planos e Metas -> bg-white (Já está)

# 5. Atenção -> bg-blue theme-dark (Já está)

# 6. Materiais Educativos -> bg-white
content = content.replace(
    '<section id="materiais-educativos" class="new-section bg-blue theme-dark">',
    '<section id="materiais-educativos" class="new-section bg-white">'
)
# Fix arrows in materiais-educativos from #fff to #000
# I will only replace #fff to #000 inside the materiais-educativos section.
# Let's extract the section, modify, and put it back.
match = re.search(r'(<section id="materiais-educativos".*?</section>)', content, flags=re.DOTALL)
if match:
    sec = match.group(1)
    # The buttons have color:#fff;
    sec = sec.replace('color:#fff;', 'color:#000;')
    content = content[:match.start()] + sec + content[match.end():]

# 7. Rede de Proteção -> bg-blue theme-dark
content = content.replace(
    '<section id="rede-protecao" class="new-section bg-white" style="position:relative; overflow:hidden;">',
    '<section id="rede-protecao" class="new-section bg-blue theme-dark" style="position:relative; overflow:hidden;">'
)
# Inside rede-protecao, fix inline dark colors to white
match = re.search(r'(<section id="rede-protecao".*?</section>)', content, flags=re.DOTALL)
if match:
    sec = match.group(1)
    # color: #4b0082 -> color: #fff
    sec = sec.replace('color: #4b0082;', 'color: #fff;')
    # color: #555 -> color: #ddd
    sec = sec.replace('color: #555;', 'color: #ddd;')
    content = content[:match.start()] + sec + content[match.end():]

# 8. Serviços e Políticas Públicas -> bg-white (já está)
# But wait, we moved the order!
# Let's check the current order from the previous script:
# preciso_ajuda (1)
# dados_violencia (2)
# atividades (3)
# planos-metas (4)
# atencao (5)
# materiais-educativos (6)
# rede-protecao (7)
# servicos (8)
# portais-institucionais (9)
# sua-opiniao (10)

# 8. Serviços is bg-white. That is correct.

# 9. Portais Institucionais is bg-blue theme-dark. That is correct.

# 10. Sua Opinião Importa is bg-gray. That is correct.

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Cores alternadas com sucesso!")

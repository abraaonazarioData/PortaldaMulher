import re

file_path = r"c:\Users\Administrator\Desktop\Portal Mulher\new\Portal Mulher\django_portal_mulher\templates\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract sections
def extract_section(content, section_id):
    pattern = r'(<section id="' + section_id + r'".*?</section>)'
    match = re.search(pattern, content, flags=re.DOTALL)
    return match.group(1) if match else ""

preciso_ajuda = extract_section(content, "preciso-ajuda")
dados_violencia = extract_section(content, "dados-violencia")
materiais_educativos = extract_section(content, "materiais-educativos")
rede_protecao = extract_section(content, "rede-protecao")
servicos = extract_section(content, "servicos")

# Extract top and bottom parts
header_match = re.search(r'(.*?<main class="main-content-new">)', content, flags=re.DOTALL)
header = header_match.group(1) if header_match else ""

# The footer part after the sections
# It contains numeros-box, modal-avaliacao, etc.
footer_start = content.rfind('<div class="numeros-box"')
footer = content[footer_start:] if footer_start != -1 else ""

# Replace the numeros-box with the "Sua Opinião Importa" Layout
new_footer = """
    <!-- Seção 10: Sua Opinião Importa -->
    <section id="sua-opiniao" class="new-section bg-gray">
        <div class="container">
            <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap; gap: 20px;">
                <div style="text-align: center; color: #003670;">
                    <i class="fa-solid fa-users" style="font-size: 3rem; margin-bottom: 10px;"></i>
                    <h3 style="font-size: 2rem; margin: 0;">{{ visit_count }}</h3>
                    <p style="font-weight: bold; text-transform: uppercase;">Acessos ao Portal</p>
                </div>
                <div style="text-align: center;">
                    <a href="#" onclick="abrirModalAvaliacao(event)" style="display: inline-block; background: #2855a8; color: white; padding: 20px 40px; border-radius: 8px; text-decoration: none; font-size: 1.5rem; font-weight: bold;">
                        <i class="fa-solid fa-comments"></i> Fale Cidadão
                    </a>
                </div>
            </div>
        </div>
    </section>
"""

# Include the modal and script from the original footer
if '<!-- Modal de Avaliação -->' in footer:
    modal_start = footer.find('<!-- Modal de Avaliação -->')
    new_footer += "\n" + footer[modal_start:]

# 3. Atividades
sec_atividades = """
    <!-- Seção 3: Atividades -->
    <section id="atividades" class="new-section bg-blue theme-dark">
        <div class="container">
            <div class="new-section-header">
                <div class="new-section-title"><span class="pipe">|</span>Atividades em Destaque</div>
                <div class="new-section-line"></div>
            </div>
            <div style="display: flex; gap: 20px; overflow-x: auto; padding: 20px 0;">
                <!-- Placeholder cards -->
                <div style="background: white; color: #333; padding: 20px; border-radius: 8px; min-width: 250px;">
                    <img src="{% static 'cards/BI.png' %}" style="width: 100%; height: 150px; object-fit: cover; border-radius: 4px; margin-bottom: 10px;">
                    <h4 style="color: #003670;">Título da Atividade</h4>
                    <p style="font-size: 0.9rem;">Descrição breve da atividade realizada.</p>
                </div>
                <div style="background: white; color: #333; padding: 20px; border-radius: 8px; min-width: 250px;">
                    <img src="{% static 'cards/BI.png' %}" style="width: 100%; height: 150px; object-fit: cover; border-radius: 4px; margin-bottom: 10px;">
                    <h4 style="color: #003670;">Título da Atividade</h4>
                    <p style="font-size: 0.9rem;">Descrição breve da atividade realizada.</p>
                </div>
                <div style="background: white; color: #333; padding: 20px; border-radius: 8px; min-width: 250px;">
                    <img src="{% static 'cards/BI.png' %}" style="width: 100%; height: 150px; object-fit: cover; border-radius: 4px; margin-bottom: 10px;">
                    <h4 style="color: #003670;">Título da Atividade</h4>
                    <p style="font-size: 0.9rem;">Descrição breve da atividade realizada.</p>
                </div>
            </div>
        </div>
    </section>
"""

# 4. Planos e Metas
sec_planos = """
    <!-- Seção 4: Planos e Metas -->
    <section id="planos-metas" class="new-section bg-white">
        <div class="container">
            <div class="new-section-header">
                <div class="new-section-title"><span class="pipe">|</span>Planos e Metas</div>
                <div class="new-section-line"></div>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 40px; align-items: center;">
                <div style="flex: 1; min-width: 300px; text-align: center;">
                    <img src="{% static 'assets/puzzle_goals.png' %}" alt="Objetivo e Meta" style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);">
                </div>
                <div style="flex: 1; min-width: 300px; font-size: 1.1rem; line-height: 1.6; color: #555;">
                    <p>O Portal Mato Grosso se dedica à proteção da mulher no Estado, buscando o cumprimento dos objetivos e metas estabelecidos pela Secretaria de Estado de Segurança Pública e por todos os órgãos da Rede de Proteção.</p>
                    <p><strong>Nosso objetivo central:</strong> erradicar a violência e promover a autonomia.</p>
                </div>
            </div>
        </div>
    </section>
"""

# 5. Atenção
sec_atencao = """
    <!-- Seção 5: Atenção -->
    <section id="atencao" class="new-section bg-blue theme-dark">
        <div class="container">
            <div style="background: rgba(255, 255, 255, 0.1); border-left: 5px solid #ffcc00; padding: 30px; border-radius: 0 8px 8px 0;">
                <span style="background: #ffcc00; color: #000; padding: 5px 15px; font-weight: bold; font-size: 1.2rem; border-radius: 4px; margin-bottom: 20px; display: inline-block;">Atenção</span>
                <p style="font-size: 1.1rem; margin-top: 10px; line-height: 1.6;">Informamos que no período de 06 de julho até o término das eleições, este site terá atualizações paralisadas pela legislação eleitoral com foco em serviços públicos.</p>
                <p style="font-size: 1.1rem; font-weight: bold; margin-top: 20px;">As publicações em nossas redes sociais ficarão suspensas no período.</p>
            </div>
        </div>
    </section>
"""

# 9. Portais Institucionais
sec_portais = """
    <!-- Seção 9: Portais Institucionais -->
    <section id="portais-institucionais" class="new-section bg-blue theme-dark">
        <div class="container">
            <div class="new-section-header">
                <div class="new-section-title"><span class="pipe">|</span>Portais Institucionais</div>
                <div class="new-section-line"></div>
            </div>
            <div style="display: flex; gap: 20px; overflow-x: auto; padding: 20px 0; align-items: center; justify-content: center; background: white; border-radius: 8px; padding: 30px;">
                <div style="color: #333; font-weight: bold; font-size: 1.2rem;">SECOM</div>
                <div style="width: 2px; height: 30px; background: #ddd;"></div>
                <div style="color: #333; font-weight: bold; font-size: 1.2rem;">SEPLAG</div>
                <div style="width: 2px; height: 30px; background: #ddd;"></div>
                <div style="color: #333; font-weight: bold; font-size: 1.2rem;">SESP</div>
                <div style="width: 2px; height: 30px; background: #ddd;"></div>
                <div style="color: #333; font-weight: bold; font-size: 1.2rem;">CASA CIVIL</div>
            </div>
        </div>
    </section>
"""

new_html = "\n\n".join([
    header,
    preciso_ajuda,
    dados_violencia,
    sec_atividades,
    sec_planos,
    sec_atencao,
    materiais_educativos,
    rede_protecao,
    servicos,
    sec_portais,
    new_footer
])

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Layout da Home reorganizado com sucesso!")

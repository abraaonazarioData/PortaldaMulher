import re

file_path = r"c:\Users\Administrator\Desktop\Portal Mulher\new\Portal Mulher\django_portal_mulher\templates\index.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix Planos e Metas Image size
old_planos_img = 'style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 10px 20px rgba(0,0,0,0.1);"'
new_planos_img = 'style="max-width: 350px; max-height: 250px; object-fit: contain; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 0 auto; display: block;"'
content = content.replace(old_planos_img, new_planos_img)

# 2. Standardize Atividades Cards
old_atividades_card = 'style="background: white; color: #333; padding: 20px; border-radius: 8px; min-width: 250px;"'
new_atividades_card = 'style="background: white; color: #333; padding: 20px; border-radius: 8px; min-width: 250px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.2s;" onmouseover="this.style.transform=\'translateY(-5px)\'" onmouseout="this.style.transform=\'translateY(0)\'"'
content = content.replace(old_atividades_card, new_atividades_card)

# Standardize Atividades Images
old_atividades_img = 'style="width: 100%; height: 150px; object-fit: cover; border-radius: 4px; margin-bottom: 10px;"'
new_atividades_img = 'style="width: 100%; height: 170px; object-fit: cover; border-radius: 8px; margin-bottom: 15px;"'
content = content.replace(old_atividades_img, new_atividades_img)

# 3. Standardize Materiais Educativos Cards
# Replace CSS in the head or inline block if exists. Let's just fix the inline ones.
# Actually, Materiais Educativos uses class="material-card" which is defined in CSS somewhere, maybe base.html.
# I'll inject a <style> block into index.html to override globally.
css_overrides = """
<style>
    /* Padronizacao Visual Premium */
    .material-card {
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        transition: transform 0.2s ease !important;
    }
    .material-card:hover {
        transform: translateY(-5px) !important;
    }
    .material-card img, .material-card iframe {
        height: 170px !important;
        border-radius: 8px 8px 0 0 !important;
        object-fit: cover !important;
    }
    .servico-card {
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        transition: transform 0.2s ease !important;
    }
    .servico-card:hover {
        transform: translateY(-5px) !important;
    }
    .servico-card img {
        height: 170px !important;
        width: 100% !important;
        object-fit: contain !important;
        border-radius: 8px !important;
    }
    .new-emergency-card {
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
</style>
"""

# Inject before </main> or at the end of the file
if "</main>" in content and "Padronizacao Visual Premium" not in content:
    content = content.replace("</main>", css_overrides + "\n</main>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Padronização aplicada com sucesso!")

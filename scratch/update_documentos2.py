import sys
import re

filepath = r'c:\Users\Administrator\Desktop\Portal Mulher\new\Portal Mulher\django_portal_mulher\templates\documentos.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS
css_old = '''  .doc-category-header {
    background-color: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    padding: 20px 28px;
    font-size: 1.25rem;
    font-weight: 800;
    color: #334155;
    display: flex;
    align-items: center;
    gap: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }'''

css_new = '''  .doc-category-header {
    background-color: #f8fafc;
    border-bottom: 1px solid #e2e8f0;
    padding: 20px 28px;
    font-size: 1.25rem;
    font-weight: 800;
    color: #334155;
    display: flex;
    align-items: center;
    justify-content: space-between;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    cursor: pointer;
    user-select: none;
  }
  
  .doc-category-header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .doc-category-toggle-icon {
    transition: transform 0.3s ease;
    color: #94a3b8;
  }

  .doc-category-card.active .doc-category-toggle-icon {
    transform: rotate(180deg);
  }

  .doc-list {
    display: none;
    flex-direction: column;
    padding: 20px;
  }
  
  .doc-category-card.active .doc-list {
    display: flex;
  }'''

content = content.replace(css_old, css_new)

content = content.replace('''  .doc-list {
    display: flex;
    flex-direction: column;
  }''', '')

search_old = '''<!-- Barra de Busca Avançada -->
<div class="doc-search-wrapper">
<input class="doc-search-input" id="docSearch" placeholder="Buscar leis, decretos ou relatórios..." type="text"/>
<i class="fa-solid fa-magnifying-glass doc-search-icon"></i>
</div>
</div>'''

search_new = '''<!-- Filtros e Busca Avançada -->
<div style="display: flex; gap: 15px; flex-wrap: wrap; flex: 1; justify-content: flex-end; align-items: center;">
    <div style="position: relative; max-width: 250px; width: 100%;">
        <select id="categoryFilter" class="doc-search-input" style="padding-left: 20px; cursor: pointer; appearance: none;">
            <option value="all">Todas as Categorias</option>
            <option value="cat-leis-federais">Leis Federais</option>
            <option value="cat-leis-estaduais">Leis Estaduais</option>
            <option value="cat-decretos-normativas">Decretos e Normativas</option>
            <option value="cat-pendente">Pendente / Outras</option>
        </select>
        <i class="fa-solid fa-chevron-down doc-search-icon" style="left: auto; right: 18px;"></i>
    </div>
    
    <div class="doc-search-wrapper" style="flex: 1; max-width: 350px;">
        <input class="doc-search-input" id="docSearch" placeholder="Buscar documento..." type="text"/>
        <i class="fa-solid fa-magnifying-glass doc-search-icon"></i>
    </div>
</div>
</div>'''
content = content.replace(search_old, search_new)

def repl_header(m):
    id_val = m.group(1)
    inner_icon = m.group(2)
    inner_text = m.group(3).strip()
    
    active_class = ' active' if id_val == 'cat-leis-federais' else ''
    
    return f'''<div class="doc-category-card{active_class}" id="{id_val}">
<div class="doc-category-header" onclick="toggleCategory('{id_val}')">
    <div class="doc-category-header-left">
        {inner_icon}
        {inner_text}
    </div>
    <i class="fa-solid fa-chevron-down doc-category-toggle-icon"></i>
</div>'''

pattern = r'<div class="doc-category-card" id="([^"]+)"(?: [^>]*)?>\s*<div class="doc-category-header">\s*(<i class="fa-solid [^"]+"></i>)\s*([^<]+)\s*</div>'
content = re.sub(pattern, repl_header, content)


js_old = '''<script>
  document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("docSearch");
    const docItems = document.querySelectorAll(".doc-item");
    const docCategories = document.querySelectorAll(".doc-category-card");

    searchInput.addEventListener("input", function () {
      const query = searchInput.value
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .trim();

      docCategories.forEach((category) => {
        let categoryHasMatch = false;
        const items = category.querySelectorAll(".doc-item");

        items.forEach((item) => {
          const titleText = item
            .querySelector(".doc-item-title")
            .textContent.toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");
          const descText = item
            .querySelector(".doc-item-desc")
            .textContent.toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");

          if (titleText.includes(query) || descText.includes(query)) {
            item.classList.remove("hidden-doc");
            categoryHasMatch = true;
          } else {
            item.classList.add("hidden-doc");
          }
        });

        // Se houver correspondência, exibe a categoria, senão esconde
        // O card de "Estudos" tem comportamento especial porque não possui itens listados de forma padrão (só o empty state)
        if (category.id === "cat-estudos") {
          if (query === "") {
            category.classList.remove("hidden-doc");
          } else {
            // Oculta Estudos se estiver buscando por algo específico e não houver correspondência (já que Estudos está vazio)
            category.classList.add("hidden-doc");
          }
        } else {
          if (categoryHasMatch || query === "") {
            category.classList.remove("hidden-doc");
          } else {
            category.classList.add("hidden-doc");
          }
        }
      });
    });
  });
</script>'''


js_new = '''<script>
  function toggleCategory(categoryId) {
      const card = document.getElementById(categoryId);
      if(card) {
          card.classList.toggle("active");
      }
  }

  document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("docSearch");
    const categoryFilter = document.getElementById("categoryFilter");
    const docCategories = document.querySelectorAll(".doc-category-card");

    function applyFilters() {
      const query = searchInput.value
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .trim();
        
      const selectedCategory = categoryFilter.value;

      docCategories.forEach((category) => {
        let categoryHasMatch = false;
        
        if (selectedCategory !== 'all' && category.id !== selectedCategory) {
            category.style.display = 'none';
            return;
        } else {
            category.style.display = 'block'; 
        }

        const items = category.querySelectorAll(".doc-item");
        items.forEach((item) => {
          const titleText = item
            .querySelector(".doc-item-title")
            .textContent.toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");
          const descText = item
            .querySelector(".doc-item-desc")
            .textContent.toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");

          if (titleText.includes(query) || descText.includes(query)) {
            item.classList.remove("hidden-doc");
            categoryHasMatch = true;
          } else {
            item.classList.add("hidden-doc");
          }
        });

        if (categoryHasMatch || query === "") {
          category.classList.remove("hidden-doc");
          // Expandir a categoria se houver busca
          if (query !== "") {
              category.classList.add("active");
          }
        } else {
          category.classList.add("hidden-doc");
        }
      });
    }

    searchInput.addEventListener("input", applyFilters);
    categoryFilter.addEventListener("change", applyFilters);
  });
</script>'''

content = content.replace(js_old, js_new)

# Remove the inline style padding and gap from doc-list since CSS handles it
content = content.replace('<div style="display: flex; flex-direction: column; gap: 20px;">', '<div>')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully.")

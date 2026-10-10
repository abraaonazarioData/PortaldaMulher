import sys
import re

filepath = r'c:\Users\Administrator\Desktop\Portal Mulher\new\Portal Mulher\django_portal_mulher\templates\documentos.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the description text since Relatórios/Estudos were removed
old_desc = "Consulte leis federais, decretos estaduais, relatórios oficiais e estudos\\n      técnicos voltados para a defesa, proteção e garantia dos direitos das\\n      mulheres em Mato Grosso."
new_desc = "Consulte leis federais, leis estaduais, decretos e normativas voltados para a defesa, proteção e garantia dos direitos das mulheres em Mato Grosso."
# Using regex to replace description loosely in case of spacing issues
content = re.sub(r'Consulte leis federais, decretos estaduais, relatórios oficiais e estudos\s+técnicos voltados para a defesa, proteção e garantia dos direitos das\s+mulheres em Mato Grosso.', new_desc, content)


# 2. Improve Accordion Animation with CSS Grid & fix Search Input Styles
css_to_add = '''  /* UX Improvements */
  .doc-category-card {
    transition: all 0.3s ease;
  }
  
  .doc-list-wrapper {
    display: grid;
    grid-template-rows: 0fr;
    transition: grid-template-rows 0.3s ease-out;
  }
  
  .doc-category-card.active .doc-list-wrapper {
    grid-template-rows: 1fr;
  }
  
  .doc-list-inner {
    overflow: hidden;
  }
  
  .doc-category-header:hover {
    background-color: #f1f5f9;
  }

  .doc-search-input {
    height: 52px; /* Ensure both inputs have exact same height */
    box-sizing: border-box;
  }
  
  select.doc-search-input {
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2394a3b8'%3E%3Cpath d='M7 10l5 5 5-5z'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 15px center;
    background-size: 20px;
  }
'''

# insert before </style>
content = content.replace('</style>', css_to_add + '\n</style>')

# Remove old `.doc-list` display logic since we'll use CSS grid
content = content.replace('''  .doc-list {
    display: none;
    flex-direction: column;
    padding: 20px;
  }
  
  .doc-category-card.active .doc-list {
    display: flex;
  }''', '''  .doc-list {
    display: flex;
    flex-direction: column;
  }''')


# 3. Fix the HTML layout for doc-list to support CSS grid animation
# Replace `<div class="doc-list">` with `<div class="doc-list-wrapper"><div class="doc-list-inner"><div class="doc-list">`
content = content.replace('<div class="doc-list">', '<div class="doc-list-wrapper"><div class="doc-list-inner"><div class="doc-list">')
# And we need to close the extra two divs for each doc-list.
# The pattern is `<div class="doc-list"> ... </div>\n</div>\n</div>` 
# We'll just replace the closing parts.
# Let's use a regex to match the end of doc-category-card
content = re.sub(r'(</div>\s*)</div>\s*<!-- CATEGORIA', r'\1</div></div></div>\n\n<!-- CATEGORIA', content)
# For the last one (Pendente):
content = re.sub(r'(</div>\s*)</div>\s*</main>', r'\1</div></div></div>\n\n</main>', content)

# 4. Remove inline styles from doc-item to make them clean lists instead of boxed cards
content = content.replace('padding: 20px; border: 1px solid #eee; border-radius: 8px; background: #f9f9f9;', 'padding: 20px 28px;')

# 5. Fix filter HTML (remove manual chevron for select, as we added it via CSS background)
content = content.replace('<i class="fa-solid fa-chevron-down doc-search-icon" style="left: auto; right: 18px;"></i>', '')

# Ensure the search wrappers have consistent gap and alignment
content = content.replace('gap: 15px; flex-wrap: wrap; flex: 1; justify-content: flex-end; align-items: center;', 'gap: 15px; flex-wrap: wrap; flex: 1; justify-content: flex-end; align-items: flex-start;')


with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("UX updated successfully.")

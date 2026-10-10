import re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace title styles to have fixed height and flex centering
old_style = 'style="display: block; font-size: 1rem; font-weight: 700; color: #004b87; margin-bottom: 12px; min-height: 40px; text-align: center;"'
new_style = 'style="display: flex; align-items: center; justify-content: center; font-size: 1rem; font-weight: 700; color: #004b87; margin-bottom: 12px; height: 75px; text-align: center;"'

content = content.replace(old_style, new_style)

# Some of the tags were <span>, let's change them to <div> just in case flex behaves weird on inline elements, but display: flex automatically makes it block-level.
# Still, I will leave it as span if it already works, but replacing span with div for the titles is safer.
# To be safe, I'll just rely on display: flex.

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')

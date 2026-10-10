import os
import glob

# Path to the templates directory
templates_dir = r'c:\Users\Administrator\Desktop\Portal Mulher\new\Portal Mulher\django_portal_mulher\templates'

for root, _, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check if it contains mojibake
            if 'Ã§' in content or 'Ã£' in content or 'Ã³' in content or 'Ãª' in content or 'Ã¡' in content:
                try:
                    fixed_content = content.encode('latin1').decode('utf-8')
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)
                    print(f"Fixed encoding for {file_path}")
                except Exception as e:
                    print(f"Could not fix {file_path}: {e}")

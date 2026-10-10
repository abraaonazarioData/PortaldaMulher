import os
import ftfy

templates_dir = r'c:\Users\Administrator\Desktop\Portal Mulher\new\Portal Mulher\django_portal_mulher\templates'

for root, _, files in os.walk(templates_dir):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if it has the specific mojibake patterns
                if 'Ã' in content:
                    fixed_content = ftfy.fix_text(content)
                    if fixed_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(fixed_content)
                        print(f"Fixed {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

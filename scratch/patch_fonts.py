import os
import glob
import re

templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
html_files = glob.glob(os.path.join(templates_dir, "*.html"))

font_link = '<link rel="stylesheet" href="/static/css/theme-fonts.css">'

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # 1. Update <html lang="te"> to dynamic language
    if '<html lang="te">' in content:
        content = content.replace('<html lang="te">', '<html lang="{{ current_lang if current_lang else \'te\' }}">')
        modified = True
    elif '<html lang=' in content and 'current_lang' not in content:
        content = re.sub(r'<html lang="[^"]*">', '<html lang="{{ current_lang if current_lang else \'te\' }}">', content)
        modified = True

    # 2. Add theme-fonts.css if not present
    if '/static/css/theme-fonts.css' not in content:
        if '<head>' in content:
            content = content.replace('<head>', '<head>\n  ' + font_link, 1)
            modified = True

    # 3. Replace hardcoded font-family in body CSS
    if "font-family: 'Segoe UI', 'Arial', sans-serif;" in content:
        content = content.replace("font-family: 'Segoe UI', 'Arial', sans-serif;", "font-family: inherit;")
        modified = True
    
    if 'font-family: "Segoe UI", sans-serif;' in content:
        content = content.replace('font-family: "Segoe UI", sans-serif;', 'font-family: inherit;')
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched: {os.path.basename(filepath)}")
    else:
        print(f"No changes needed: {os.path.basename(filepath)}")

print("Font patching complete!")

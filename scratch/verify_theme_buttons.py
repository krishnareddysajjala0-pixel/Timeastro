import os
import glob

templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
html_files = glob.glob(os.path.join(templates_dir, "*.html"))

themes = ['default', 'cosmic', 'sunset', 'luxury', 'cyberpunk', 'solar', 'mandala', 'twilight', 'aurora']

theme_buttons_html = '''<div class="theme-options">
        <button class="theme-btn" data-theme-btn="default" onclick="setTheme('default')" title="Bright Mode (Default)"><i class="fas fa-sun"></i></button>
        <button class="theme-btn" data-theme-btn="cosmic" onclick="setTheme('cosmic')" title="Cosmic Mode"><i class="fas fa-moon"></i></button>
        <button class="theme-btn" data-theme-btn="sunset" onclick="setTheme('sunset')" title="Sunset"><i class="fas fa-cloud-sun"></i></button>
        <button class="theme-btn" data-theme-btn="luxury" onclick="setTheme('luxury')" title="Obsidian Gold"><i class="fas fa-gem"></i></button>
        <button class="theme-btn" data-theme-btn="cyberpunk" onclick="setTheme('cyberpunk')" title="Neo Cyber"><i class="fas fa-bolt"></i></button>
        <button class="theme-btn" data-theme-btn="solar" onclick="setTheme('solar')" title="Solar Amber"><i class="fas fa-fire-alt"></i></button>
        <button class="theme-btn" data-theme-btn="mandala" onclick="setTheme('mandala')" title="Royal Mandala"><i class="fas fa-dharmachakra"></i></button>
        <button class="theme-btn" data-theme-btn="twilight" onclick="setTheme('twilight')" title="Twilight Fusion"><i class="fas fa-adjust"></i></button>
        <button class="theme-btn" data-theme-btn="aurora" onclick="setTheme('aurora')" title="Divine Aurora"><i class="fas fa-magic"></i></button>
      </div>'''

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    missing = [t for t in themes if f'data-theme-btn="{t}"' not in content]
    if missing:
        print(f"File {os.path.basename(filepath)} is missing theme buttons: {missing}")
    else:
        print(f"File {os.path.basename(filepath)} has all 9 theme buttons!")


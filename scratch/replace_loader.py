import os
import re

template_dir = 'templates'
for filename in os.listdir(template_dir):
    if filename.endswith('.html'):
        path = os.path.join(template_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace 6-3=6 with Calculating text
        content = re.sub(
            r'element\.innerHTML = \'<div class="rainbow-scroller">6-3=6</div>\';',
            r'element.innerHTML = \'గణన చేస్తోంది...\';',
            content
        )
        
        # Remove rainbow scroller CSS block (multi-line)
        content = re.sub(
            r'/\* Rainbow Scroller Styles \*/.*?document\.head\.appendChild\(style.*?\);',
            '',
            content,
            flags=re.DOTALL
        )
        # Also matching the other variant: // Inject Rainbow Scroller Styles
        content = re.sub(
            r'// Inject Rainbow Scroller Styles.*?document\.head\.appendChild\(style.*?\);',
            '',
            content,
            flags=re.DOTALL
        )

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

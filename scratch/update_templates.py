import os
import re

files_to_update = [
    'templates/chart.html',
    'templates/compare_results.html',
    'templates/transit_partial.html',
    'templates/results.html',
    'templates/daily_panchangam.html'
]

replacements = [
    (r'\.rasi-name', '.lagna-name'),
    (r'class="rasi-name"', 'class="lagna-name"'),
    (r'class=\'rasi-name\'', 'class="lagna-name"'),
    (r'macro box\(rasi\)', 'macro box(lagna)'),
    (r'macro box_p1\(rasi\)', 'macro box_p1(lagna)'),
    (r'macro box_p2\(rasi\)', 'macro box_p2(lagna)'),
    (r'\{\{\s*rasi\s*\}\}', '{{ lagna }}'),
    (r'\[rasi\]', '[lagna]'),
    (r'==rasi', '==lagna'),
    (r'bhava-rasi-tag', 'bhava-lagna-tag')
]

for file_path in files_to_update:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        for pattern, replacement in replacements:
            new_content = re.sub(pattern, replacement, new_content)
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {file_path}")
        else:
            print(f"No changes for {file_path}")

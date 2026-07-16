import glob

for f in glob.glob('templates/*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('RAVAN ASTRO', 'Thraitha Siddantha Jyothisyam').replace('Ravan Astro', 'Thraitha Siddantha Jyothisyam')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

for f in glob.glob('translations/*.json'):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('RAVAN ASTRO', 'Thraitha Siddantha Jyothisyam').replace('Ravan Astro', 'Thraitha Siddantha Jyothisyam')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

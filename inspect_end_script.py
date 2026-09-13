import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\KRISH\.gemini\antigravity\scratch\Timeastro\templates\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

end_script = html.rfind('</script>')
if end_script != -1:
    print(html[end_script-500:end_script+9])

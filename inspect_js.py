import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\KRISH\.gemini\antigravity\scratch\Timeastro\templates\index.html', encoding='utf-8') as f:
    html = f.read()

start = html.find('function getCurrentLocation')
if start != -1:
    print(html[start:start+1200])

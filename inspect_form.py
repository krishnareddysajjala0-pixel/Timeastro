import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\KRISH\.gemini\antigravity\scratch\Timeastro\templates\index.html', encoding='utf-8') as f:
    html = f.read()

# Find form tag and inputs
start = html.find('<form')
end = html.find('</form>', start)
if start != -1 and end != -1:
    print(html[start:min(start+2000, len(html))])

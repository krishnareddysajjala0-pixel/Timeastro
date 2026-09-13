import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\KRISH\.gemini\antigravity\scratch\Timeastro\app.py', 'r', encoding='utf-8') as f:
    code = f.read()

target = 'def get_kundali_data(name, dob, tob, place, lat, lon):'
replacement = '''def get_kundali_data(name, dob, tob, place, lat, lon):
    try:
        lat = float(lat) if lat is not None else 17.3850
    except (ValueError, TypeError):
        lat = 17.3850

    try:
        lon = float(lon) if lon is not None else 78.4867
    except (ValueError, TypeError):
        lon = 78.4867

    if not dob or len(str(dob).strip()) < 8:
        dob = datetime.datetime.now().strftime("%Y-%m-%d")

    if not tob or len(str(tob).strip()) < 3:
        tob = datetime.datetime.now().strftime("%H:%M")
'''

if target in code and 'try:\n        lat = float(lat) if lat is not None' not in code:
    code = code.replace(target, replacement)

with open(r'C:\Users\KRISH\.gemini\antigravity\scratch\Timeastro\app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Patched get_kundali_data with default lat/lon/dob/tob fallbacks!")

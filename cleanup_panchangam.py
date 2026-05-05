import os
import re

templates_dir = "templates"

# 1. Remove button from all html files
pattern = re.compile(r'<button[^>]*onclick="window\.location\.href=\'/panchangam\'"[^>]*>.*?<\/button>\s*', re.DOTALL)

for file in os.listdir(templates_dir):
    if file.endswith(".html"):
        filepath = os.path.join(templates_dir, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = pattern.sub('', content)
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Removed button from {file}")

# 2. Delete templates/panchangam.html
panchangam_file = os.path.join(templates_dir, "panchangam.html")
if os.path.exists(panchangam_file):
    os.remove(panchangam_file)
    print("Deleted templates/panchangam.html")

# 3. Remove route from app.py
app_py_path = "app.py"
with open(app_py_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

route_pattern = re.compile(r'@app\.route\("/panchangam"\)\ndef panchangam\(\):.*?return render_template\("panchangam\.html", \*\*birth_info\)\s*', re.DOTALL)
new_app_content = route_pattern.sub('', app_content)

if new_app_content != app_content:
    with open(app_py_path, 'w', encoding='utf-8') as f:
        f.write(new_app_content)
    print("Removed route /panchangam from app.py")

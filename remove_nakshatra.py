import os
import re

templates_dir = "templates"

# 1. Remove goToCorrection JS and button from all html files
js_pattern = re.compile(r'\s*function goToCorrection\(\) \{.*?\n\s*\}\s*', re.DOTALL)
button_pattern = re.compile(r'<button[^>]*onclick="goToCorrection\(\)"[^>]*>.*?<\/button>\s*', re.DOTALL)

for file in os.listdir(templates_dir):
    if file.endswith(".html"):
        filepath = os.path.join(templates_dir, file)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = js_pattern.sub('', content)
        new_content = button_pattern.sub('', new_content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Removed goToCorrection from {file}")

# 2. Delete templates/manual_correction.html
mc_file = os.path.join(templates_dir, "manual_correction.html")
if os.path.exists(mc_file):
    os.remove(mc_file)
    print("Deleted templates/manual_correction.html")

# 3. Remove route /manual_nakshatra from app.py
app_py_path = "app.py"
with open(app_py_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

# Remove the /manual_nakshatra route entirely
route_pattern = re.compile(r'@app\.route\("/manual_nakshatra", methods=\["POST"\]\)\ndef manual_nakshatra\(\):.*?return render_template\(\s*"manual_correction\.html".*?\)\s*', re.DOTALL)
app_content = route_pattern.sub('\n\n', app_content)

# Remove the correction_type check block in routes (chart2, chart3, etc)
correction_block_pattern = re.compile(r'\s*# Check for manual correction submission\s*correction_type = request\.form\.get\("correction_type"\)\s*if correction_type == "manual":.*?session\[\'birth_info\'\] = birth_info\s*', re.DOTALL)
app_content = correction_block_pattern.sub('\n    ', app_content)

# Are there any other correction related routes?
with open(app_py_path, 'w', encoding='utf-8') as f:
    f.write(app_content)
print("Removed manual_nakshatra routes and processing blocks from app.py")

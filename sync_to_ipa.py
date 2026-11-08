import os, shutil, glob

myastro_dir = r"C:\Users\KRISH\.gemini\antigravity\scratch\myastro"
ipa_dir = r"C:\Users\KRISH\.gemini\antigravity\scratch\ravanastro-ipa"

# 1. Copy app.py
shutil.copy2(os.path.join(myastro_dir, "app.py"), ipa_dir)

# 2. Copy astro_constants*.json
for f in glob.glob(os.path.join(myastro_dir, "astro_constants*.json")):
    shutil.copy2(f, ipa_dir)

# 3. Copy templates
ipa_templates = os.path.join(ipa_dir, "templates")
for f in glob.glob(os.path.join(myastro_dir, "templates", "*.html")):
    shutil.copy2(f, ipa_templates)

# 4. Copy static
ipa_static = os.path.join(ipa_dir, "static")
if os.path.exists(os.path.join(myastro_dir, "static")):
    for root, dirs, files in os.walk(os.path.join(myastro_dir, "static")):
        rel = os.path.relpath(root, os.path.join(myastro_dir, "static"))
        dest_root = os.path.join(ipa_static, rel)
        os.makedirs(dest_root, exist_ok=True)
        for f in files:
            shutil.copy2(os.path.join(root, f), os.path.join(dest_root, f))

# 5. Copy translations
ipa_trans = os.path.join(ipa_dir, "translations")
for f in glob.glob(os.path.join(myastro_dir, "translations", "*.json")):
    os.makedirs(ipa_trans, exist_ok=True)
    shutil.copy2(f, ipa_trans)

# 6. Copy ios_src/App/App/public or www if exists
www_dir = os.path.join(ipa_dir, "www")
if os.path.exists(www_dir):
    print("Found www directory in ipa")

print("Successfully synced myastro to ravanastro-ipa!")

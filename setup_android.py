import os
import shutil
import glob

base_dir = os.path.dirname(os.path.abspath(__file__))
android_dir = os.path.join(base_dir, "android_app")
python_dst = os.path.join(android_dir, "app", "src", "main", "python")
java_dst = os.path.join(android_dir, "app", "src", "main", "java", "com", "timeastro", "app")
res_values_dst = os.path.join(android_dir, "app", "src", "main", "res", "values")

os.makedirs(python_dst, exist_ok=True)
os.makedirs(java_dst, exist_ok=True)
os.makedirs(res_values_dst, exist_ok=True)

# Copy python backend & resources
shutil.copy2(os.path.join(base_dir, "app.py"), python_dst)

for pattern in ["astro_constants*.json", "bhava_lord_rules*.json", "detailed_bhava_meanings*.json"]:
    for f in glob.glob(os.path.join(base_dir, pattern)):
        shutil.copy2(f, python_dst)

for fname in ["astro_qa_rules.txt", "extracted_rules.txt", "user_data.txt"]:
    src_f = os.path.join(base_dir, fname)
    if os.path.exists(src_f):
        shutil.copy2(src_f, python_dst)

# Copy directories
for dir_name in ["templates", "static", "translations"]:
    src_d = os.path.join(base_dir, dir_name)
    dst_d = os.path.join(python_dst, dir_name)
    if os.path.exists(src_d):
        if os.path.exists(dst_d):
            shutil.rmtree(dst_d)
        shutil.copytree(src_d, dst_d)

print("Python files and directories copied successfully to:", python_dst)

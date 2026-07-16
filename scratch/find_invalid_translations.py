import os
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

translations_dir = r"C:\Users\gnana\.gemini\antigravity\scratch\Timeastro\translations"

# Telugu unicode range: \u0c00-\u0c7f
telugu_re = re.compile(r'[\u0c00-\u0c7f]')

for filename in os.listdir(translations_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(translations_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        print(f"File: {filename}")
        count = 0
        for k, v in data.items():
            if telugu_re.search(v):
                print(f"  Key: {k!r}")
                print(f"  Val: {v!r}")
                print("-" * 40)
                count += 1
        print(f"Total entries with Telugu in {filename}: {count}\n")

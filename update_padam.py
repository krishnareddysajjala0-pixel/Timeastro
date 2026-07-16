import json
import os

translations = {
    'en': { "పాదం": "Pada" },
    'hi': { "పాదం": "पद" },
    'ta': { "పాదం": "பாதம்" },
    'kn': { "పాదం": "ಪಾದ" },
    'ml': { "పాదం": "പാദം" },
    'or': { "పాదం": "ପାଦ" }
}

paths = [
    r"C:\Users\gnana\.gemini\antigravity\scratch\Timeastro\translations",
    r"C:\Users\gnana\.gemini\antigravity\scratch\YugAstro\translations"
]

for base_path in paths:
    for lang, new_words in translations.items():
        filepath = os.path.join(base_path, f"translations_{lang}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            updated = False
            for k, v in new_words.items():
                if k not in data or data[k] != v:
                    data[k] = v
                    updated = True
            
            if updated:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"Updated {filepath}")

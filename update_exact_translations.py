import json
import os

translations = {
    'en': {
        "పూర్తి నక్షత్ర పరిమాణం:": "Total Nakshatra Duration:",
        "నక్షత్ర భుక్తి:": "Nakshatra Elapsed:",
        "నక్షత్ర భోగ్యం:": "Nakshatra Remaining:",
        "దశ భుక్తి:": "Dasa Elapsed:",
        "దశ భోగ్యం:": "Dasa Remaining:"
    },
    'hi': {
        "పూర్తి నక్షత్ర పరిమాణం:": "संपूर्ण नक्षत्र प्रमाण:",
        "నక్షత్ర భుక్తి:": "नक्षत्र भुक्ति (बीता हुआ):",
        "నక్షత్ర భోగ్యం:": "नक्षत्र भोग्य (शेष):",
        "దశ భుక్తి:": "दशा भुक्ति (बीता हुआ):",
        "దశ భోగ్యం:": "दशा भोग्य (शेष):"
    },
    'ta': {
        "పూర్తి నక్షత్ర పరిమాణం:": "நட்சத்திர முழு அளவு:",
        "నక్షత్ర భుక్తి:": "நட்சத்திர புக்தி:",
        "నక్షత్ర భోగ్యం:": "நட்சத்திர போக்யம்:",
        "దశ భుక్తి:": "தசை புக்தி:",
        "దశ భోగ్యం:": "தசை போக்யம்:"
    },
    'kn': {
        "పూర్తి నక్షత్ర పరిమాణం:": "ಪೂರ್ಣ ನಕ್ಷತ್ರ ಪ್ರಮಾಣ:",
        "నక్షత్ర భుక్తి:": "ನಕ್ಷತ್ರ ಭುಕ್ತಿ (ಕಳೆದ):",
        "నక్షత్ర భోగ్యం:": "ನಕ್ಷತ್ರ ಭೋಗ್ಯ (ಉಳಿದ):",
        "దశ భుక్తి:": "ದಶಾ ಭುಕ್ತಿ:",
        "దశ భోగ్యం:": "ದಶಾ ಭೋಗ್ಯ:"
    },
    'ml': {
        "పూర్తి నక్షత్ర పరిమాణం:": "പൂർണ്ണ നക്ഷത്ര പ്രമാണം:",
        "నక్షత్ర భుక్తి:": "നക്ഷത്ര ഭുക്തി:",
        "నక్షత్ర భోగ్యం:": "നക്ഷത്ര ഭോഗ്യം:",
        "దశ భుక్తి:": "ദശാ ഭുക്തി:",
        "దశ భోగ్యం:": "ദശാ ഭോഗ്യം:"
    },
    'or': {
        "పూర్తి నక్షత్ర పరిమాణం:": "ପୂର୍ଣ୍ଣ ନକ୍ଷତ୍ର ପରିମାଣ:",
        "నక్షత్ర భుక్తి:": "ନକ୍ଷତ୍ର ଭୁକ୍ତି:",
        "నక్షత్ర భోగ్యం:": "ନକ୍ଷତ୍ର ଭୋଗ୍ୟ:",
        "దశ భుక్తి:": "ଦଶା ଭୁକ୍ତି:",
        "దశ భోగ్యం:": "ଦଶା ଭୋଗ୍ୟ:"
    }
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
            else:
                print(f"No changes for {filepath}")

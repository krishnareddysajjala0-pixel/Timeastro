import json
import os
import glob

translations = {
    'en': {
        "జన్మ నక్షత్రం, పాదం:": "Birth Nakshatra, Pada:",
        "గతించిన కాలం:": "Elapsed Time:",
        "మిగిలిన కాలం:": "Remaining Time:",
        "జన్మ దశ:": "Birth Dasa:",
        "గత కాలం:": "Elapsed Period:",
        "భోగ్య కాలం:": "Remaining Period:",
        "ప్రస్తుత దశ - అంతర్దశ:": "Current Dasa - Antardasa:"
    },
    'hi': {
        "జన్మ నక్షత్రం, పాదం:": "जन्म नक्षत्र, पद:",
        "గతించిన కాలం:": "बीता हुआ समय:",
        "మిగిలిన కాలం:": "शेष समय:",
        "జన్మ దశ:": "जन्म दशा:",
        "గత కాలం:": "बीता हुआ काल:",
        "భోగ్య కాలం:": "भोग्य काल:",
        "ప్రస్తుత దశ - అంతర్దశ:": "वर्तमान दशा - अंतर्दशा:"
    },
    'ta': {
        "జన్మ నక్షత్రం, పాదం:": "பிறந்த நட்சத்திரம், பாதம்:",
        "గతించిన కాలం:": "கடந்த காலம்:",
        "మిగిలిన కాలం:": "மீதமுள்ள காலம்:",
        "జన్మ దశ:": "பிறப்பு தசை:",
        "గత కాలం:": "கடந்த காலம்:",
        "భోగ్య కాలం:": "மீதமுள்ள காலம்:",
        "ప్రస్తుత దశ - అంతర్దశ:": "தற்போதைய தசை - அந்தர்தசை:"
    },
    'kn': {
        "జన్మ నక్షత్రం, పాదం:": "ಜನ್ಮ ನಕ್ಷತ್ರ, ಪಾದ:",
        "గతించిన కాలం:": "ಕಳೆದ ಸಮಯ:",
        "మిగిలిన కాలం:": "ಉಳಿದ ಸಮಯ:",
        "జన్మ దశ:": "ಜನ್ಮ ದಶೆ:",
        "గత కాలం:": "ಕಳೆದ ಕಾಲ:",
        "భోగ్య కాలం:": "ಉಳಿದ ಕಾಲ:",
        "ప్రస్తుత దశ - అంతర్దశ:": "ಪ್ರಸ್ತುತ ದಶೆ - ಅಂತರ್ದಶೆ:"
    },
    'ml': {
        "జన్మ నక్షత్రం, పాదం:": "ജന്മ നക്ഷത്രം, പാദം:",
        "గతించిన కాలం:": "കഴിഞ്ഞ സമയം:",
        "మిగిలిన కాలం:": "ബാക്കി സമയം:",
        "జన్మ దశ:": "ജന്മ ദശ:",
        "గత కాలం:": "കഴിഞ്ഞ കാലം:",
        "భోగ్య కాలం:": "ബാക്കി കാലം:",
        "ప్రస్తుత దశ - అంతర్దశ:": "നിലവിലെ ദശ - അന്തരദശ:"
    },
    'or': {
        "జన్మ నక్షత్రం, పాదం:": "ଜନ୍ମ ନକ୍ଷତ୍ର, ପଦ:",
        "గతించిన కాలం:": "ବିତିଯାଇଥିବା ସମୟ:",
        "మిగిలిన కాలం:": "ବାକି ସମୟ:",
        "జన్మ దశ:": "ଜନ୍ମ ଦଶା:",
        "గత కాలం:": "ବିତିଯାଇଥିବା କାଳ:",
        "భోగ్య కాలం:": "ବାକି କାଳ:",
        "ప్రస్తుత దశ - అంతర్దశ:": "ବର୍ତ୍ତମାନ ଦଶା - ଅନ୍ତର୍ଦଶା:"
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

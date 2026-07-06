import os
import json
import re

PROJECT_DIR = r"C:\Users\gnana\.gemini\antigravity\scratch\YugAstro"

# Correct mappings for translations_{lang}.json
VOCAB_CORRECTIONS = {
    'en': {
        'భూమి': 'Earth',
        'చిత్ర': 'Chitra',
        'మిత్ర': 'Mitra',
        'బుధుడు': 'Mercury',
        'బుధ': 'Mercury',
        'గురువు': 'Jupiter',
        'గురు': 'Jupiter',
        'సూర్యుడు': 'Sun',
        'సూర్య': 'Sun',
        'చంద్రుడు': 'Moon',
        'చంద్ర': 'Moon',
        'కుజుడు': 'Mars',
        'శుక్రుడు': 'Venus',
        'శని': 'Saturn',
        'రాహు': 'Rahu',
        'కేతు': 'Ketu',
        'గురు వర్గము': 'Jupiter Party',
        'శని వర్గము': 'Saturn Party',
        'జాఫతకము': 'Birth Plan',
        'జాఫతకము ఫలితాలు': 'Birth Plan Results',
        'జాఫతకము పోలిక': 'Birth Plan Comparison',
        'జాతక ఫలితము (Detailed Analysis)': 'Birth Plan Result (Detailed Analysis)',
        'పుట్టినప్పుడే నిర్ణయించబడిన పతకము కావున దీనిని జాఫతకము అంటున్నాము.': 'Since it is a plan determined at the time of birth, we call it a Birth Plan.',
        'ద్వాదశ గ్రహములతో కూడిన జ్యోతిష్య శాస్త్రము ఆధారముగా మీ జాఫతకము నిర్ణయించబడుతుంది.': 'Your Birth Plan is determined based on astrology with Dwadasa planets.'
    },
    'hi': {
        'భూమి': 'पृथ्वी',
        'చిత్ర': 'चित्र',
        'మిత్ర': 'मित्र',
        'బుధుడు': 'बुध',
        'బుధ': 'बुध',
        'గురువు': 'गुरु',
        'గురు': 'गुरु',
        'సూర్యుడు': 'सूर्य',
        'చంద్రుడు': 'चंद्र',
        'జాఫతకము': 'जन्म योजना',
        'జాఫతకము ఫలితాలు': 'जन्म योजना परिणाम',
        'జాఫతకము పోలిక': 'जन्म योजना तुलना'
    },
    'kn': {
        'భూమి': 'ಭೂಮಿ',
        'చిత్ర': 'ಚಿತ್ರ',
        'ಮಿತ್ರ': 'ಮಿತ್ರ',
        'బుధుడు': 'ಬುಧ',
        'బుధ': 'ಬುಧ',
        'గురువు': 'ಗುರು',
        'గురు': 'ಗುರು',
        'సూర్యుడు': 'ಸೂರ್ಯ',
        'చంద్రుడు': 'ಚಂದ್ರ',
        'జాఫతకము': 'ಜನ್ಮ ಯೋಜನೆ',
        'జాఫతకము ఫలితాలు': 'ಜನ್ಮ ಯೋಜನೆ ಫಲಿತಾಂಶಗಳು',
        'జాఫతకము పోಲಿಕ': 'ಜನ್ಮ ಯೋಜನೆ ಹೋಲಿಕೆ'
    },
    'ta': {
        'భూమి': 'பூமி',
        'చిత్ర': 'சித்ரா',
        'మిత్ర': 'மித்ரா',
        'బుధుడు': 'புதன்',
        'బుధ': 'புதன்',
        'గురువు': 'குரு',
        'గురు': 'குரு',
        'సూర్యుడు': 'சூரியன்',
        'చంద్రుడు': 'சந்திரன்',
        'జాఫతకము': 'பிறப்புத் திட்டம்',
        'జాఫతకము ఫలితాలు': 'பிறப்புத் திட்ட முடிவுகள்',
        'జాఫతకము పోలిక': 'பிறப்புத் திட்ட ஒப்பீடு'
    },
    'ml': {
        'భూమి': 'ഭൂമി',
        'చిత్ర': 'ചിത്ര',
        'మిత్ర': 'മിത്ര',
        'బుధుడు': 'ബുധൻ',
        'బుధ': 'ബുധൻ',
        'గురువు': 'ഗുരു',
        'గురు': 'ഗുരു',
        'సూర్యుడు': 'സൂര്യൻ',
        'చంద్రుడు': 'ചന്ദ്രൻ',
        'జాఫతకము': 'ജനന പദ്ധതി',
        'జాఫతకము ఫలితాలు': 'ജനന പദ്ധതി ഫലങ്ങൾ',
        'జాఫతకము పోలిక': 'ജനന പദ്ധതി താരതമ്യം'
    },
    'or': {
        'భూమి': 'ପୃଥିବୀ',
        'చిత్ర': 'ଚିତ୍ର',
        'මିତ୍ର': 'ମିତ୍ର',
        'బుధుడు': 'ବୁଧ',
        'బుధ': 'ବୁଧ',
        'గురువు': 'ଗୁରୁ',
        'ଗୁରୁ': 'ଗୁରୁ',
        'సూర్యుడు': 'ସୂର୍ଯ୍ୟ',
        'చంద్రుడు': 'ଚନ୍ଦ୍ର',
        'జాఫతకము': 'ଜନ୍ମ ଯୋଜନା',
        'జాఫతకము ఫలితాలు': 'ଜନ୍ମ ଯୋଜନା ଫଳାଫଳ',
        'జాఫతకము ଅନୁରୂପ': 'ଜନ୍ମ ଯୋଜନା ତୁଳନା'
    }
}

# Description corrections for each language's rule files
def correct_text_en(text):
    if not isinstance(text, str):
        return text
        
    # Replace "the sun"/"the moon" (case-insensitive) with "Sun"/"Moon"
    text = re.sub(r'\bthe\s+sun\b', 'Sun', text, flags=re.IGNORECASE)
    text = re.sub(r'\bthe\s+moon\b', 'Moon', text, flags=re.IGNORECASE)
    
    # Capitalize all planet names and remove weekday names or generic translations
    text = re.sub(r'\bWednesday\b', 'Mercury', text)
    text = re.sub(r'\bWed\b', 'Mercury', text)
    text = re.sub(r'\bThursday\b', 'Jupiter', text)
    text = re.sub(r'\bTeacher\b', 'Jupiter', text)
    text = re.sub(r'\bteacher\b', 'Jupiter', text)
    text = re.sub(r'\ba friend\b', 'Mitra', text)
    text = re.sub(r'\bfriend\b', 'Mitra', text)
    text = re.sub(r'\bpicture\b', 'Chitra', text)
    text = re.sub(r'\bPicture\b', 'Chitra', text)
    text = re.sub(r'\bland\b', 'Earth', text)
    text = re.sub(r'\bLand\b', 'Earth', text)
    
    # Class / Party replacements
    text = re.sub(r'\bGuru\s+Varga\b', 'Jupiter Party', text)
    text = re.sub(r'\bGuru\s+class\b', 'Jupiter Party', text)
    text = re.sub(r'\bGuru\s+group\b', 'Jupiter Party', text)
    text = re.sub(r'\bShani\s+varga\b', 'Saturn Party', text)
    text = re.sub(r'\bShani\s+class\b', 'Saturn Party', text)
    text = re.sub(r'\bShani\s+group\b', 'Saturn Party', text)
    text = re.sub(r'\bSaturn\s+class\b', 'Saturn Party', text)
    text = re.sub(r'\bSaturn\s+group\b', 'Saturn Party', text)
    text = re.sub(r'\bGuru\s+party\b', 'Jupiter Party', text)
    text = re.sub(r'\bShani\s+party\b', 'Saturn Party', text)
    text = re.sub(r'\bguru\s+party\b', 'Jupiter Party', text)
    text = re.sub(r'\bshani\s+party\b', 'Saturn Party', text)
    
    # Horoscope / Birth chart -> Birth Plan
    text = re.sub(r'\bhoroscope\b', 'Birth Plan', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbirth\s+chart\b', 'Birth Plan', text, flags=re.IGNORECASE)
    text = re.sub(r'\bbirth\s+plan\b', 'Birth Plan', text, flags=re.IGNORECASE)
    
    # Global capitalize for planets
    planets_list = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu', 'earth', 'chitra', 'mitra']
    for p in planets_list:
        text = re.sub(r'\b' + p + r'\b', p.capitalize(), text, flags=re.IGNORECASE)
        
    return text

def correct_text_hi(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r'\bबुधवार\b', 'बुध', text)
    text = re.sub(r'\bगुरुवार\b', 'गुरु', text)
    text = re.sub(r'\bशिक्षक\b', 'गुरु', text)
    text = re.sub(r'\bएक दोस्त\b', 'मित्र', text)
    text = re.sub(r'\bदोस्त\b', 'मित्र', text)
    text = re.sub(r'\bजन्म\s+कुंडली\b', 'जन्म योजना', text)
    text = re.sub(r'\bकुंडली\b', 'जन्म योजना', text)
    return text

def correct_text_kn(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r'\bಬುಧವಾರ\b', 'ಬುಧ', text)
    text = re.sub(r'\bಗುರುವಾರ\b', 'ಗುರು', text)
    text = re.sub(r'\bಶಿಕ್ಷಕ\b', 'ಗುರು', text)
    text = re.sub(r'\bಒಬ್ಬ ಸ್ನೇಹಿತ\b', 'ಮಿತ್ರ', text)
    text = re.sub(r'\bಸ್ನೇಹಿತ\b', 'ಮಿತ್ರ', text)
    text = re.sub(r'\bಜನ್ಮ\s+ಕುಂಡಲಿ\b', 'ಜನ್ಮ ಯೋಜನೆ', text)
    text = re.sub(r'\bಕುಂಡಲಿ\b', 'ಜನ್ಮ ಯೋಜನೆ', text)
    return text

def correct_text_ta(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r'\bவியாழன்\b', 'குரு', text)
    text = re.sub(r'\bஆசிரியர்\b', 'குரு', text)
    text = re.sub(r'\bஒரு நண்பர்\b', 'மித்ரா', text)
    text = re.sub(r'\bநண்பர்\b', 'மித்ரா', text)
    text = re.sub(r'\bபடம்\b', 'சித்ரா', text)
    text = re.sub(r'\bஜாதகம்\b', 'பிறப்புத் திட்டம்', text)
    return text

def correct_text_ml(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r'\bಬುಧನಾഴ്ച\b', 'ಬುಧನ್', text)
    text = re.sub(r'\bവ്യാഴാഴ്ച\b', 'ഗുരു', text)
    text = re.sub(r'\bഅധ്യാപകൻ\b', 'ഗുരു', text)
    text = re.sub(r'\bഒരു സുഹൃത്ത്\b', 'മിത്ര', text)
    text = re.sub(r'\bസുഹൃത്ത്\b', 'മിത്ര', text)
    text = re.sub(r'\bചിത്രം\b', 'ചിത്ര', text)
    text = re.sub(r'\bജാതകം\b', 'ജനന പദ്ധതി', text)
    return text

def correct_text_or(text):
    if not isinstance(text, str):
        return text
    text = re.sub(r'\bଗୁରୁବାର\b', 'ଗୁରୁ', text)
    text = re.sub(r'\bଶିକ୍ଷକ\b', 'ଗୁରୁ', text)
    text = re.sub(r'\bଜଣେ ବନ୍ଧୁ\b', 'ମିତ୍ର', text)
    text = re.sub(r'\bବନ୍ଧୁ\b', 'ମିତ୍ର', text)
    text = re.sub(r'\bଛବି\b', 'ଚିତ୍ର', text)
    text = re.sub(r'\bକୋଷ୍ଠୀ\b', 'ଜନ୍ମ ଯୋଜନା', text)
    return text

CORRECT_FUNCTIONS = {
    'en': correct_text_en,
    'hi': correct_text_hi,
    'kn': correct_text_kn,
    'ta': correct_text_ta,
    'ml': correct_text_ml,
    'or': correct_text_or
}

def correct_file(filepath, correct_fn):
    if not os.path.exists(filepath):
        return
    print(f"Correcting {os.path.basename(filepath)}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    def process_node(node):
        if isinstance(node, str):
            return correct_fn(node)
        elif isinstance(node, list):
            return [process_node(item) for item in node]
        elif isinstance(node, dict):
            return {k: process_node(v) for k, v in node.items()}
        return node
        
    new_data = process_node(data)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)

def main():
    # 1. Correct vocabularies translations_*.json
    for lang, corrections in VOCAB_CORRECTIONS.items():
        vocab_path = os.path.join(PROJECT_DIR, "translations", f"translations_{lang}.json")
        if os.path.exists(vocab_path):
            print(f"Updating vocabulary translations_{lang}.json...")
            with open(vocab_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for k, v in corrections.items():
                data[k] = v
            with open(vocab_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
    # 2. Correct description files for rules
    for lang, correct_fn in CORRECT_FUNCTIONS.items():
        bhava_rules_path = os.path.join(PROJECT_DIR, f"bhava_lord_rules_{lang}.json")
        meanings_path = os.path.join(PROJECT_DIR, f"detailed_bhava_meanings_{lang}.json")
        
        correct_file(bhava_rules_path, correct_fn)
        correct_file(meanings_path, correct_fn)
        
    print("Corrections applied successfully!")

if __name__ == "__main__":
    main()

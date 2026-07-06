import os
import json
import requests
import urllib.parse
import time

PROJECT_DIR = r"C:\Users\gnana\.gemini\antigravity\scratch\YugAstro"
TRANSLATIONS_DIR = os.path.join(PROJECT_DIR, "translations")
os.makedirs(TRANSLATIONS_DIR, exist_ok=True)

# Target languages (excluding English and Telugu)
LANGUAGES = {
    'kn': 'kn',
    'hi': 'hi',
    'ta': 'ta',
    'ml': 'ml',
    'or': 'or'
}

# Manual overrides for short grammatical fragments and time units
MANUAL_OVERRIDES = {
    "గం": {"en": "h", "kn": "ಗಂ", "hi": "घं", "ta": "மணி", "ml": "മണി", "or": "ଘଣ୍ଟା"},
    "ని": {"en": "m", "kn": "ನಿ", "hi": "मि", "ta": "நிமி", "ml": "മിനി", "or": "ମି"},
    "సం": {"en": "y", "kn": "ವರ್ಷ", "hi": "वर्ष", "ta": "வரு", "ml": "വർഷം", "or": "ବର୍ଷ"},
    "నెలలు": {"en": "m", "kn": "ತಿಂಗಳು", "hi": "महीने", "ta": "மாதங்கள்", "ml": "മാസം", "or": "ମାସ"},
    "ఉ: ": {"en": "AM: ", "kn": "ಬె: ", "hi": "पूर्वाहन: ", "ta": "முற்பகல்: ", "ml": "രാവിലെ: ", "or": "ପୂର୍ବାହ୍ନ: "},
    "సా: ": {"en": "PM: ", "kn": "సా: ", "hi": "अपराह्न: ", "ta": "பிற்பகல்: ", "ml": "వైകുന്നేരം: ", "or": "ଅପରାହ୍ନ: "},
    "ఉ": {"en": "AM", "kn": "ಬె", "hi": "पूर्वाहन", "ta": "முற்பகல்", "ml": "രാവിലെ", "or": "ପୂର୍ବାହ୍ന"},
    "సా": {"en": "PM", "kn": "సా", "hi": "अपраह्न", "ta": "பிற்பகல்", "ml": "വൈകുന്നేരം", "or": "ଅପରାହ୍న"},
    "నుంచి": {"en": "from", "kn": "ఇಂದ", "hi": "से", "ta": "இருந்து", "ml": "നിന്ന്", "or": "ଠାରୁ"},
    "వరకు": {"en": "to", "kn": "ವರೆಗೆ", "hi": "तक", "ta": "வரை", "ml": "വരെ", "or": "ପର୍ଯ୍ୟନ୍ତ"},
    "నుండి": {"en": "from", "kn": "ఇಂದ", "hi": "से", "ta": "இருந்து", "ml": "നിന്ന്", "or": "ଠାରు"},
    "రేపు": {"en": "tomorrow", "kn": "నాಳೆ", "hi": "कल", "ta": "நாளை", "ml": "ನಾಳೆ", "or": "ଆସନ୍ତାକಾଲિ"},
    "నిన్న": {"en": "yesterday", "kn": "ನಿನ್ನೆ", "hi": "कल (बीता)", "ta": "நேற்று", "ml": "இன்னಲೆ", "or": "ଗତକାଲି"},
    "ప్రస్తుతం": {"en": "present", "kn": "ಪ್ರಸ್ತುತ", "hi": "वर्तमान", "ta": "தற்போதைய", "ml": "നിലവിലെ", "or": "ବର୍ତ୍ତମାନ"},
    "గతం": {"en": "past", "kn": "ಹಿಂದಿನ", "hi": "भूतकाल", "ta": "கடந்த காலம்", "ml": "കഴിഞ്ഞ കാലം", "or": "ଅତୀତ"},
    "భవిష్యత్తు": {"en": "future", "kn": "ಭವಿಷ್ಯ", "hi": "भವಿಷ್ಯ", "ta": "எதிர்காலம்", "ml": "ഭാവി", "or": "ଭବିଷ୍ୟତ"},
    "వ తిథి": {"en": " Tithi", "kn": "ನೇ తిథి", "hi": "वीं तिथि", "ta": "வது திதி", "ml": "–ാം തിഥി", "or": "ତମ ତିଥି"},
    "వ పాదం": {"en": " Pada", "kn": "ನೇ ಪಾದ", "hi": "चरण", "ta": "வது பாதம்", "ml": "–ാം പാദം", "or": "ପାଦ"},
    "గురు వర్గము": {"en": "Jupiter Group", "kn": "గురు వర్గ", "hi": "गुरु वर्ग", "ta": "குரு வர்க்கம்", "ml": "ഗുരു വർഗ്ഗം", "or": "ଗୁରୁ ବର୍ଗ"},
    "శని వర్గము": {"en": "Saturn Group", "kn": "శని వర్గ", "hi": "शनि वर्ग", "ta": "சனி வர்க்கம்", "ml": "ଶନି ବର୍ଗ"}
}

def translate_mymemory(text, target_lang, src_lang='en'):
    if not text or not text.strip():
        return ""
    
    # Handle manual override first
    for te_key, mappings in MANUAL_OVERRIDES.items():
        if text.strip() == te_key or text.strip() == mappings.get('en', ''):
            return mappings.get(target_lang, text)
            
    # Try translating
    url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(text)}&langpair={src_lang}|{target_lang}&de=astrologytranslation@myastro.com"
    
    for attempt in range(2):
        try:
            time.sleep(1.5) # Polite sleep for individual requests
            r = requests.get(url, timeout=12)
            if r.status_code == 200:
                data = r.json()
                translated = data['responseData']['translatedText']
                if translated:
                    return translated.strip()
            elif r.status_code == 429:
                print(f"[{target_lang}] MyMemory rate limit on individual. Sleeping 10 seconds.")
                time.sleep(10)
            else:
                time.sleep(2)
        except Exception:
            time.sleep(2)
            
    return text

def translate_mymemory_batch(texts, target_lang, src_lang='en'):
    if not texts:
        return []
    
    results = [None] * len(texts)
    
    # Pre-fill overrides
    for idx, text in enumerate(texts):
        for te_key, mappings in MANUAL_OVERRIDES.items():
            if text.strip() == te_key or text.strip() == mappings.get('en', ''):
                results[idx] = mappings.get(target_lang, text)
                break
                
    # Group untranslated
    untranslated_indices = [idx for idx, val in enumerate(results) if val is None]
    if not untranslated_indices:
        return results
        
    untranslated_texts = [texts[idx] for idx in untranslated_indices]
    
    batches = []
    current_batch = []
    current_length = 0
    
    for idx, text in zip(untranslated_indices, untranslated_texts):
        if len(current_batch) >= 20 or (current_length + len(text) > 1000):
            batches.append(current_batch)
            current_batch = []
            current_length = 0
        current_batch.append((idx, text))
        current_length += len(text)
        
    if current_batch:
        batches.append(current_batch)
        
    print(f"[{target_lang}] Batching {len(untranslated_texts)} strings in {len(batches)} batches using newlines.")
    
    for b_idx, batch in enumerate(batches):
        indices, batch_texts = zip(*batch)
        query = '\n'.join(batch_texts)
        success = False
        retries = 3
        
        while retries > 0 and not success:
            try:
                time.sleep(2.5) # Polite sleep between batches
                url = f"https://api.mymemory.translated.net/get?q={urllib.parse.quote(query)}&langpair={src_lang}|{target_lang}&de=astrologytranslation@myastro.com"
                r = requests.get(url, timeout=15)
                
                if r.status_code == 200:
                    data = r.json()
                    translated_query = data['responseData']['translatedText']
                    if translated_query:
                        translated_batch = [item.strip() for item in translated_query.split('\n')]
                        
                        if len(translated_batch) == len(batch):
                            for j, val in enumerate(translated_batch):
                                results[indices[j]] = val
                            success = True
                            print(f"[{target_lang}] Batch {b_idx + 1}/{len(batches)} completed successfully.")
                        else:
                            print(f"[{target_lang}] Batch {b_idx + 1} size mismatch (got {len(translated_batch)}/{len(batch)}). Retrying...")
                            retries -= 1
                            time.sleep(2)
                elif r.status_code == 429:
                    print(f"[{target_lang}] MyMemory rate limit. Sleeping 12 seconds.")
                    time.sleep(12)
                    retries -= 1
                else:
                    time.sleep(2)
                    retries -= 1
            except Exception as e:
                print(f"[{target_lang}] Exception in batch {b_idx + 1}: {e}")
                time.sleep(2)
                retries -= 1
                
        if not success:
            print(f"[{target_lang}] Batch {b_idx + 1} failed. Falling back to individual translation.")
            for j, text in enumerate(batch_texts):
                idx = indices[j]
                results[idx] = translate_mymemory(text, target_lang, src_lang)
                
    return results

def translate_bhava_lord_rules(target_lang):
    dest_path = os.path.join(PROJECT_DIR, f"bhava_lord_rules_{target_lang}.json")
    if os.path.exists(dest_path):
        print(f"File {dest_path} already exists. Skipping.")
        return
        
    print(f"Translating bhava_lord_rules.json to {target_lang}...")
    source_path = os.path.join(PROJECT_DIR, "bhava_lord_rules_en.json")
    with open(source_path, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
        
    keys_list = []
    texts_list = []
    
    for house, lords in en_data.items():
        for lord, rule_dict in lords.items():
            for field, text in rule_dict.items():
                if text:
                    keys_list.append((house, lord, field))
                    texts_list.append(text)
                
    translated_texts = translate_mymemory_batch(texts_list, target_lang, 'en')
    
    new_data = {}
    for house, lords in en_data.items():
        new_data[house] = {}
        for lord, rule_dict in lords.items():
            new_data[house][lord] = rule_dict.copy()
            
    for (house, lord, field), trans in zip(keys_list, translated_texts):
        new_data[house][lord][field] = trans
        
    with open(dest_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {dest_path}")

def translate_detailed_bhava_meanings(target_lang):
    dest_path = os.path.join(PROJECT_DIR, f"detailed_bhava_meanings_{target_lang}.json")
    if os.path.exists(dest_path):
        print(f"File {dest_path} already exists. Skipping.")
        return
        
    print(f"Translating detailed_bhava_meanings.json to {target_lang}...")
    source_path = os.path.join(PROJECT_DIR, "detailed_bhava_meanings_en.json")
    with open(source_path, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
        
    keys_list = []
    texts_list = []
    
    for house, fields in en_data.items():
        for key, text in fields.items():
            if text and key in ["title", "meaning", "shubha", "paapa", "neutral"]:
                keys_list.append((house, key))
                texts_list.append(text)
                
    translated_texts = translate_mymemory_batch(texts_list, target_lang, 'en')
    
    new_data = {}
    for house, fields in en_data.items():
        new_data[house] = fields.copy()
        
    for (house, key), trans in zip(keys_list, translated_texts):
        new_data[house][key] = trans
        
    with open(dest_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {dest_path}")

def translate_astro_constants(target_lang):
    dest_path = os.path.join(PROJECT_DIR, f"astro_constants_{target_lang}.json")
    if os.path.exists(dest_path):
        print(f"File {dest_path} already exists. Skipping.")
        return
        
    print(f"Translating astro_constants.json to {target_lang}...")
    source_path = os.path.join(PROJECT_DIR, "astro_constants_en.json")
    with open(source_path, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
        
    paths = []
    texts = []
    
    def collect_strings(obj, path):
        if isinstance(obj, str):
            paths.append(path)
            texts.append(obj)
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                collect_strings(item, path + [idx])
        elif isinstance(obj, dict):
            for k, v in obj.items():
                collect_strings(v, path + [k])
                
    collect_strings(en_data, [])
    
    translated_texts = translate_mymemory_batch(texts, target_lang, 'en')
    
    def set_nested(obj, path, val):
        for key in path[:-1]:
            obj = obj[key]
        obj[path[-1]] = val
        
    new_data = json.loads(json.dumps(en_data))
    for path, trans in zip(paths, translated_texts):
        set_nested(new_data, path, trans)
        
    with open(dest_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {dest_path}")

def translate_vocabularies(target_lang):
    dest_path = os.path.join(TRANSLATIONS_DIR, f"translations_{target_lang}.json")
    if os.path.exists(dest_path):
        print(f"File {dest_path} already exists. Skipping.")
        return
        
    print(f"Translating combined vocabulary for {target_lang}...")
    en_vocab_path = os.path.join(TRANSLATIONS_DIR, "translations_en.json")
    with open(en_vocab_path, 'r', encoding='utf-8') as f:
        en_vocab = json.load(f)
        
    telugu_keys = list(en_vocab.keys())
    english_values = [en_vocab[k] for k in telugu_keys]
    
    translated_values = translate_mymemory_batch(english_values, target_lang, 'en')
    
    mapping = {}
    for k, trans in zip(telugu_keys, translated_values):
        mapping[k] = trans
        
    with open(dest_path, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"Saved vocabulary to {dest_path}")

def main():
    for code, name in LANGUAGES.items():
        print(f"\n===== PROCESSING LANGUAGE: {name} =====")
        translate_bhava_lord_rules(code)
        translate_detailed_bhava_meanings(code)
        translate_astro_constants(code)
        translate_vocabularies(code)
        print(f"===== FINISHED {name} =====\n")
        
if __name__ == "__main__":
    main()

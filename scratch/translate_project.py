import os
import json
import requests
import urllib.parse
import time

PROJECT_DIR = r"C:\Users\gnana\.gemini\antigravity\scratch\YugAstro"
TRANSLATIONS_DIR = os.path.join(PROJECT_DIR, "translations")
os.makedirs(TRANSLATIONS_DIR, exist_ok=True)

LANGUAGES = {
    'en': 'en',
    'kn': 'kn',
    'hi': 'hi',
    'ta': 'ta',
    'ml': 'ml',
    'or': 'or'
}

def translate_batch(texts, target_lang, src_lang='te'):
    if not texts:
        return []
    
    results = [None] * len(texts)
    
    # Safe limits for GET requests: max 10 items or 150 Telugu characters (which URL-encodes to ~1350 characters)
    batches = []
    current_batch = []
    current_length = 0
    
    for idx, text in enumerate(texts):
        if len(current_batch) >= 10 or (current_length + len(text) > 150):
            batches.append(current_batch)
            current_batch = []
            current_length = 0
        current_batch.append((idx, text))
        current_length += len(text)
        
    if current_batch:
        batches.append(current_batch)
        
    print(f"[{target_lang}] Translating {len(texts)} strings in {len(batches)} batches using GET...")
    
    for b_idx, batch in enumerate(batches):
        indices, batch_texts = zip(*batch)
        query = ' ___ '.join(batch_texts)
        success = False
        retries = 3
        
        while retries > 0 and not success:
            try:
                time.sleep(1.5) # Polite delay
                encoded_query = urllib.parse.quote(query)
                url = f"https://translate.googleapis.com/translate_a/single?client=at&sl={src_lang}&tl={target_lang}&dt=t&q={encoded_query}"
                r = requests.get(url, timeout=20)
                
                if r.status_code == 200:
                    parts = [p[0] for p in r.json()[0] if p[0]]
                    joined = ''.join(parts)
                    translated_batch = [item.strip() for item in joined.split('___')]
                    translated_batch = [item for item in translated_batch if item]
                    
                    if len(translated_batch) == len(batch):
                        for j, val in enumerate(translated_batch):
                            results[indices[j]] = val
                        success = True
                        print(f"[{target_lang}] Batch {b_idx + 1}/{len(batches)} translated successfully.")
                    else:
                        print(f"[{target_lang}] Batch {b_idx + 1} size mismatch (got {len(translated_batch)}/{len(batch)}). Retrying...")
                        retries -= 1
                        time.sleep(2)
                elif r.status_code == 429:
                    print(f"[{target_lang}] Hit 429 Rate Limit. Sleeping for 30 seconds. Retries left: {retries}")
                    time.sleep(30)
                    retries -= 1
                else:
                    print(f"[{target_lang}] HTTP error {r.status_code}. Retrying in 4 seconds...")
                    time.sleep(4)
                    retries -= 1
            except Exception as e:
                print(f"[{target_lang}] Exception: {e}. Retrying in 4 seconds...")
                time.sleep(4)
                retries -= 1
                
        if not success:
            print(f"[{target_lang}] Batch {b_idx + 1} failed or mismatched. Splitting into sub-batches of 3.")
            sub_batches = [batch[k:k+3] for k in range(0, len(batch), 3)]
            for s_idx, s_batch in enumerate(sub_batches):
                s_indices, s_batch_texts = zip(*s_batch)
                s_query = ' ___ '.join(s_batch_texts)
                s_success = False
                s_retries = 3
                while s_retries > 0 and not s_success:
                    try:
                        time.sleep(2.0)
                        encoded_s_query = urllib.parse.quote(s_query)
                        url = f"https://translate.googleapis.com/translate_a/single?client=at&sl={src_lang}&tl={target_lang}&dt=t&q={encoded_s_query}"
                        r = requests.get(url, timeout=15)
                        if r.status_code == 200:
                            parts = [p[0] for p in r.json()[0] if p[0]]
                            joined = ''.join(parts)
                            translated_s_batch = [item.strip() for item in joined.split('___')]
                            translated_s_batch = [item for item in translated_s_batch if item]
                            if len(translated_s_batch) == len(s_batch):
                                for j, val in enumerate(translated_s_batch):
                                    results[s_indices[j]] = val
                                s_success = True
                            else:
                                s_retries -= 1
                                time.sleep(2)
                        elif r.status_code == 429:
                            print(f"[{target_lang}] Sub-batch hit 429. Sleeping 30s.")
                            time.sleep(30)
                            s_retries -= 1
                        else:
                            time.sleep(3)
                            s_retries -= 1
                    except Exception:
                        time.sleep(3)
                        s_retries -= 1
                if not s_success:
                    for j, text in enumerate(s_batch_texts):
                        results[s_indices[j]] = text
                        
    return results

def translate_bhava_lord_rules(target_lang):
    dest_path = os.path.join(PROJECT_DIR, f"bhava_lord_rules_{target_lang}.json")
    if os.path.exists(dest_path):
        print(f"File {dest_path} already exists. Skipping.")
        return
        
    print(f"Translating bhava_lord_rules.json to {target_lang}...")
    source_path = os.path.join(PROJECT_DIR, "bhava_lord_rules.json")
    with open(source_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    keys_list = []
    texts_list = []
    
    for house, lords in data.items():
        for lord, rule_dict in lords.items():
            for field, text in rule_dict.items():
                if text:
                    keys_list.append((house, lord, field))
                    texts_list.append(text)
                
    translated_texts = translate_batch(texts_list, target_lang)
    
    new_data = {}
    for house, lords in data.items():
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
    source_path = os.path.join(PROJECT_DIR, "detailed_bhava_meanings.json")
    with open(source_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    keys_list = []
    texts_list = []
    
    for house, fields in data.items():
        for key, text in fields.items():
            if text and key in ["title", "meaning", "shubha", "paapa", "neutral"]:
                keys_list.append((house, key))
                texts_list.append(text)
                
    translated_texts = translate_batch(texts_list, target_lang)
    
    new_data = {}
    for house, fields in data.items():
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
    source_path = os.path.join(PROJECT_DIR, "astro_constants.json")
    with open(source_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    def collect_telugu(obj, path, collected):
        if isinstance(obj, str):
            if any('\u0c00' <= char <= '\u0c7f' for char in obj):
                collected.append((path, obj))
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                collect_telugu(item, path + [idx], collected)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                collect_telugu(v, path + [k], collected)
                
    collected = []
    collect_telugu(data, [], collected)
    
    if collected:
        paths, texts = zip(*collected)
        translated_texts = translate_batch(list(texts), target_lang)
        
        def set_nested(obj, path, val):
            for key in path[:-1]:
                obj = obj[key]
            obj[path[-1]] = val
            
        new_data = json.loads(json.dumps(data))
        for path, trans in zip(paths, translated_texts):
            set_nested(new_data, path, trans)
    else:
        new_data = data
        
    with open(dest_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {dest_path}")

def translate_vocabularies(target_lang):
    dest_path = os.path.join(TRANSLATIONS_DIR, f"translations_{target_lang}.json")
    if os.path.exists(dest_path):
        print(f"File {dest_path} already exists. Skipping.")
        return
        
    print(f"Translating combined vocabulary for {target_lang}...")
    
    template_strings_path = os.path.join(PROJECT_DIR, "scratch", "template_telugu_strings.json")
    with open(template_strings_path, 'r', encoding='utf-8') as f:
        template_strings = json.load(f)
        
    app_strings_path = os.path.join(PROJECT_DIR, "scratch", "app_telugu_strings.json")
    with open(app_strings_path, 'r', encoding='utf-8') as f:
        app_strings = json.load(f)
        
    all_strings = list(set(template_strings + app_strings))
    all_strings = [s.strip() for s in all_strings if s.strip()]
    
    print(f"Total vocabulary size: {len(all_strings)} strings.")
    
    translated_strings = translate_batch(all_strings, target_lang)
    
    mapping = {}
    for orig, trans in zip(all_strings, translated_strings):
        mapping[orig] = trans
        
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

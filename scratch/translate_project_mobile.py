import os
import json
import requests
import urllib.parse
import re
import time

PROJECT_DIR = r"C:\Users\gnana\.gemini\antigravity\scratch\YugAstro"
TRANSLATIONS_DIR = os.path.join(PROJECT_DIR, "translations")
os.makedirs(TRANSLATIONS_DIR, exist_ok=True)

# Target languages (we will translate directly from Telugu to these)
LANGUAGES = {
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
    
    # Safe limits for mobile GET: max 8 items or 350 Telugu characters (to stay well below URL limits)
    batches = []
    current_batch = []
    current_length = 0
    
    for idx, text in enumerate(texts):
        if len(current_batch) >= 8 or (current_length + len(text) > 350):
            batches.append(current_batch)
            current_batch = []
            current_length = 0
        current_batch.append((idx, text))
        current_length += len(text)
        
    if current_batch:
        batches.append(current_batch)
        
    print(f"[{target_lang}] Translating {len(texts)} strings in {len(batches)} batches using mobile endpoint...")
    
    for b_idx, batch in enumerate(batches):
        indices, batch_texts = zip(*batch)
        # Use newline as separator
        query = '\n'.join(batch_texts)
        success = False
        retries = 3
        
        while retries > 0 and not success:
            try:
                time.sleep(1.0) # Polite delay
                encoded_query = urllib.parse.quote(query)
                url = f"https://translate.google.com/m?sl={src_lang}&tl={target_lang}&q={encoded_query}"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'
                }
                r = requests.get(url, headers=headers, timeout=15)
                
                if r.status_code == 200:
                    # Match result-container content across newlines using re.DOTALL
                    m = re.search(r'class="result-container">(.*?)</div>', r.text, re.DOTALL)
                    if m:
                        translated_query = m.group(1).strip()
                        # Unescape HTML entities
                        import html
                        translated_query = html.unescape(translated_query)
                        
                        translated_batch = [item.strip() for item in translated_query.split('\n')]
                        
                        if len(translated_batch) == len(batch):
                            for j, val in enumerate(translated_batch):
                                results[indices[j]] = val
                            success = True
                            print(f"[{target_lang}] Batch {b_idx + 1}/{len(batches)} translated successfully.")
                        else:
                            print(f"[{target_lang}] Batch {b_idx + 1} size mismatch (got {len(translated_batch)}/{len(batch)}). Retrying...")
                            retries -= 1
                            time.sleep(2)
                    else:
                        print(f"[{target_lang}] Batch {b_idx + 1} translation container not found in HTML. Retrying...")
                        retries -= 1
                        time.sleep(2)
                elif r.status_code == 429:
                    print(f"[{target_lang}] Hit 429 Rate Limit on mobile endpoint. Sleeping 12 seconds...")
                    time.sleep(12)
                    retries -= 1
                else:
                    print(f"[{target_lang}] HTTP error {r.status_code}. Retrying...")
                    time.sleep(3)
                    retries -= 1
            except Exception as e:
                print(f"[{target_lang}] Exception: {e}. Retrying...")
                time.sleep(3)
                retries -= 1
                
        if not success:
            print(f"[{target_lang}] Batch {b_idx + 1} failed. Translating individually...")
            for j, text in enumerate(batch_texts):
                idx = indices[j]
                try:
                    time.sleep(1.0)
                    encoded_val = urllib.parse.quote(text)
                    url = f"https://translate.google.com/m?sl={src_lang}&tl={target_lang}&q={encoded_val}"
                    r = requests.get(url, headers=headers, timeout=10)
                    m = re.search(r'class="result-container">(.*?)</div>', r.text, re.DOTALL)
                    if m:
                        import html
                        results[idx] = html.unescape(m.group(1).strip())
                    else:
                        results[idx] = text
                except Exception:
                    results[idx] = text
                    
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

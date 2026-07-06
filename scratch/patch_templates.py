import os
import re
import json

PROJECT_DIR = r"C:\Users\gnana\.gemini\antigravity\scratch\YugAstro"
TEMPLATES_DIR = os.path.join(PROJECT_DIR, "templates")

# Load unique Telugu strings sorted by length (longest first)
vocab_path = os.path.join(PROJECT_DIR, "scratch", "template_telugu_strings.json")
with open(vocab_path, 'r', encoding='utf-8') as f:
    telugu_strings = json.load(f)

# Sort descending by length to replace longer strings first
telugu_strings.sort(key=len, reverse=True)

# Stylesheet for language selector
LANG_SELECTOR_CSS = """
    /* Language Switcher */
    .language-switcher {
      position: absolute;
      top: 20px;
      left: 20px;
      display: flex;
      flex-direction: column;
      background: var(--card-bg, rgba(15, 23, 42, 0.9));
      padding: 6px;
      border-radius: 20px;
      border: 1px solid var(--card-border, rgba(99, 102, 241, 0.3));
      box-shadow: 0 4px 15px var(--shadow-color, rgba(0,0,0,0.5));
      z-index: 10000;
      backdrop-filter: blur(10px);
      transition: max-height 0.3s ease;
      overflow: hidden;
      max-height: 45px;
      min-width: 45px;
    }

    .language-switcher.expanded {
      max-height: 400px;
      border-radius: 12px;
      padding: 10px;
    }

    .lang-toggle-btn {
      background: transparent;
      border: none;
      font-size: 20px;
      color: var(--text-main, #ffffff);
      padding: 4px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      min-width: 30px;
      gap: 6px;
      font-weight: bold;
    }

    .lang-options {
      display: flex;
      flex-direction: column;
      gap: 4px;
      opacity: 0;
      transition: opacity 0.3s ease;
      pointer-events: none;
      margin-top: 8px;
    }

    .language-switcher.expanded .lang-options {
      opacity: 1;
      pointer-events: auto;
    }

    .lang-btn {
      background: transparent;
      border: none;
      font-size: 14px;
      color: var(--text-main, #ffffff);
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      text-align: left;
      transition: all 0.2s ease;
      text-decoration: none;
      display: block;
    }

    .lang-btn:hover {
      background: rgba(120, 120, 120, 0.2);
    }

    .lang-btn.active {
      font-weight: bold;
      background: var(--btn-show-bg, linear-gradient(135deg, #fbbf24, #f59e0b));
      color: var(--btn-show-text, #020617);
    }
"""

# HTML for language selector
LANG_SELECTOR_HTML = """
  <!-- Language Switcher -->
  <div class="language-switcher print-hide">
    <button class="lang-toggle-btn" onclick="this.parentElement.classList.toggle('expanded')" title="Change Language">
      <i class="fas fa-language"></i>
      <span style="font-size: 14px; margin-left: 2px;">{{ _('భాష') }}</span>
    </button>
    <div class="lang-options">
      <a href="/set_lang/te" class="lang-btn {% if current_lang == 'te' %}active{% endif %}">తెలుగు</a>
      <a href="/set_lang/en" class="lang-btn {% if current_lang == 'en' %}active{% endif %}">English</a>
      <a href="/set_lang/kn" class="lang-btn {% if current_lang == 'kn' %}active{% endif %}">ಕನ್ನಡ</a>
      <a href="/set_lang/hi" class="lang-btn {% if current_lang == 'hi' %}active{% endif %}">हिन्दी</a>
      <a href="/set_lang/ta" class="lang-btn {% if current_lang == 'ta' %}active{% endif %}">தமிழ்</a>
      <a href="/set_lang/ml" class="lang-btn {% if current_lang == 'ml' %}active{% endif %}">മലയാളം</a>
      <a href="/set_lang/or" class="lang-btn {% if current_lang == 'or' %}active{% endif %}">ଓଡ଼ିଆ</a>
    </div>
  </div>
"""

def patch_file(filepath):
    print(f"Patching {os.path.basename(filepath)}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Inject CSS stylesheet before </head>
    if "</head>" in content and ".language-switcher" not in content:
        style_inject = f"<style>{LANG_SELECTOR_CSS}</style>\n</head>"
        content = content.replace("</head>", style_inject)
        
    # 2. Inject HTML dropdown after <body>
    if "<body>" in content and "class=\"language-switcher" not in content:
        html_inject = f"<body>\n{LANG_SELECTOR_HTML}"
        content = content.replace("<body>", html_inject)
    elif "<body" in content and "class=\"language-switcher" not in content:
        body_match = re.search(r'<body[^>]*>', content)
        if body_match:
            body_tag = body_match.group(0)
            content = content.replace(body_tag, f"{body_tag}\n{LANG_SELECTOR_HTML}")

    # 3. Tokenize Jinja expressions to prevent double-wrapping
    placeholders = []
    
    def tokenize(text):
        jinja_pattern = re.compile(r'(\{\{.*?\}\}|\{%.*?%\}|\{#.*?#\})', re.DOTALL)
        def repl(match):
            placeholder = f"___JINJA_VAL_{len(placeholders)}___"
            placeholders.append(match.group(1))
            return placeholder
        return jinja_pattern.sub(repl, text)
        
    def restore(text):
        # Replace in reverse order to properly nest restored tags
        for idx in range(len(placeholders) - 1, -1, -1):
            text = text.replace(f"___JINJA_VAL_{idx}___", placeholders[idx])
        return text

    # Tokenize initial Jinja blocks
    content = tokenize(content)

    # 4. Translate all Telugu string instances
    for telugu_str in telugu_strings:
        if telugu_str in content:
            if "'" in telugu_str:
                replacement = f'{{{{ _("{telugu_str}") }}}}'
            else:
                replacement = f"{{{{ _('{telugu_str}') }}}}"
                
            content = content.replace(telugu_str, replacement)
            # Tokenize newly added wrapper immediately
            content = tokenize(content)
            
    # Restore all tokenized Jinja blocks
    content = restore(content)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
def main():
    for filename in os.listdir(TEMPLATES_DIR):
        if filename.endswith(".html"):
            filepath = os.path.join(TEMPLATES_DIR, filename)
            patch_file(filepath)
    print("All templates successfully patched!")

if __name__ == "__main__":
    main()

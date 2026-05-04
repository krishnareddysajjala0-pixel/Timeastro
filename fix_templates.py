
import os
import re

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace startTyping function
    pattern = r'function startTyping\s*\([^)]*\)\s*\{.*?\}'
    replacement = """function startTyping() {
        const element = document.getElementById("typing-text");
        if (!element) return;
        element.innerHTML = '<div class="rainbow-scroller">6-3=6</div>';
    }

    /* Rainbow Scroller Styles */
    const styleScroller = document.createElement('style');
    styleScroller.textContent = `
        .rainbow-scroller {
            font-size: 42px;
            font-weight: 900;
            white-space: nowrap;
            display: inline-block;
            animation: rainbow-scroll-left-right 4s linear infinite;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
            position: absolute;
            left: 0;
        }
        @keyframes rainbow-scroll-left-right {
            0% { color: #ff0000; left: -100px; }
            15% { color: #ff7f00; }
            30% { color: #ffff00; }
            45% { color: #00ff00; }
            60% { color: #0000ff; }
            75% { color: #4b0082; }
            90% { color: #8b00ff; }
            100% { color: #ff0000; left: 100%; }
        }
        #loading-overlay, #loading {
            overflow: hidden !important;
            position: relative !important;
        }
    `;
    document.head.appendChild(styleScroller);"""
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Specific logo replacements
    if 'daily_panchangam.html' in path:
        new_content = new_content.replace('<h2><i class="fas fa-calendar-alt"></i> దిన పంచాంగం</h2>', '<img src="/static/images/brand_logo.png" alt="Logo" class="title-emblem" style="width: 80px; height: auto; margin-bottom: 10px; display: block; margin-left: auto; margin-right: auto;">\\n                <h2> దిన పంచాంగం</h2>')
    elif 'calendar_view.html' in path:
        new_content = new_content.replace('<div class="header-branding">RAVAN ASTRO</div>', '<img src="/static/images/brand_logo.png" alt="Logo" class="title-emblem" style="width: 80px; height: auto; margin-bottom: 10px; display: block; margin-left: auto; margin-right: auto;">\\n        <div class="header-branding">జ్యోతిష్య క్యాలెండర్</div>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

files = [
    'templates/daily_panchangam.html',
    'templates/calendar_view.html',
    'templates/compare_results.html',
    'templates/compare_form.html',
    'templates/compare_dasha.html',
]

for f in files:
    full_path = os.path.join(os.getcwd(), f)
    if os.path.exists(full_path):
        fix_file(full_path)
        print(f"Fixed {f}")

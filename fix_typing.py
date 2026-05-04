
import os

def fix_start_typing(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    in_function = False
    replaced = False
    
    for line in lines:
        if 'function startTyping' in line and not replaced:
            in_function = True
            new_lines.append('    function startTyping() {\n')
            new_lines.append('        const element = document.getElementById("typing-text");\n')
            new_lines.append('        if (!element) return;\n')
            new_lines.append('        element.innerHTML = \'<div class="rainbow-scroller">6-3=6</div>\';\n')
            new_lines.append('    }\n')
            new_lines.append('    /* Rainbow Scroller Styles */\n')
            new_lines.append('    const styleScroller = document.createElement(\'style\');\n')
            new_lines.append('    styleScroller.textContent = `\n')
            new_lines.append('        .rainbow-scroller {\n')
            new_lines.append('            font-size: 42px;\n')
            new_lines.append('            font-weight: 900;\n')
            new_lines.append('            white-space: nowrap;\n')
            new_lines.append('            display: inline-block;\n')
            new_lines.append('            animation: rainbow-scroll-left-right 4s linear infinite;\n')
            new_lines.append('            text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);\n')
            new_lines.append('            position: absolute;\n')
            new_lines.append('            left: 0;\n')
            new_lines.append('        }\n')
            new_lines.append('        @keyframes rainbow-scroll-left-right {\n')
            new_lines.append('            0% { color: #ff0000; left: -100px; }\n')
            new_lines.append('            15% { color: #ff7f00; }\n')
            new_lines.append('            30% { color: #ffff00; }\n')
            new_lines.append('            45% { color: #00ff00; }\n')
            new_lines.append('            60% { color: #0000ff; }\n')
            new_lines.append('            75% { color: #4b0082; }\n')
            new_lines.append('            90% { color: #8b00ff; }\n')
            new_lines.append('            100% { color: #ff0000; left: 100%; }\n')
            new_lines.append('        }\n')
            new_lines.append('        #loading-overlay, #loading {\n')
            new_lines.append('            overflow: hidden !important;\n')
            new_lines.append('            position: relative !important;\n')
            new_lines.append('        }\n')
            new_lines.append('    `;\n')
            new_lines.append('    document.head.appendChild(styleScroller);\n')
            replaced = True
        elif in_function:
            if line.strip() == '}':
                in_function = False
        else:
            new_lines.append(line)
            
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

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
        fix_start_typing(full_path)
        print(f"Fixed startTyping in {f}")

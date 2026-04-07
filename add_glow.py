import os, glob

snippet = '''
<!-- APP GLOW BORDER -->
<style>
.app-glow-frame {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 99999;
    padding: 6px;
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    mask-composite: exclude;
}
.app-glow-frame::before {
    content: '';
    position: absolute;
    top: 50%; left: 50%;
    width: 150vmax; height: 150vmax;
    background: conic-gradient(from 0deg, transparent 60%, rgba(255, 215, 0, 0.6) 80%, #FFD700 100%);
    transform: translate(-50%, -50%) rotate(0deg);
    animation: appGlowSpin 4s linear infinite;
}
@keyframes appGlowSpin {
    100% { transform: translate(-50%, -50%) rotate(360deg); }
}
</style>
<div class="app-glow-frame"></div>
'''

for file in glob.glob('templates/*.html'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'app-glow-frame' not in content:
        # replace first occurrence of <body>
        content = content.replace('<body>', f'<body>{snippet}', 1)
        with open(file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Injected into {file}')
    else:
        print(f'Already injected into {file}')

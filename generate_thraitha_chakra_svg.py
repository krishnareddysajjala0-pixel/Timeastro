import math, os

out_dir = r"C:\Users\KRISH\.gemini\antigravity\scratch\myastro\static\images"
os.makedirs(out_dir, exist_ok=True)

W, H = 1000, 1080
cx, cy = 500, 480

r_outer = 400
r_mid = 265
r_bracket = 265
r_inner = 170
r_num = 135
r_center = 82

sectors = [
    {
        "num": 1, "rasi": "మేషం", "color": "#dc2626", "text_dark": False,
        "karakas": ["శరీర సంబంధ", "అవయవములు"],
        "punya_left": "పుణ్యము", "punya_right": "పుణ్యము"
    },
    {
        "num": 2, "rasi": "వృషభం", "color": "#facc15", "text_dark": True,
        "karakas": ["వాక్కు", "ఆయుష్షు"],
        "punya_left": "పుణ్యము", "punya_right": "పాపము"
    },
    {
        "num": 3, "rasi": "మిథునం", "color": "#84cc16", "text_dark": True,
        "karakas": ["ధన సంబంధ", "తండ్రి సంబంధ"],
        "punya_left": "పాపము", "punya_right": "పాపము"
    },
    {
        "num": 4, "rasi": "కర్కాటకం", "color": "#1d4ed8", "text_dark": False,
        "karakas": ["స్థిరాస్తులు"],
        "punya_left": "పాపము", "punya_right": "పుణ్యము"
    },
    {
        "num": 5, "rasi": "సింహం", "color": "#db2777", "text_dark": False,
        "karakas": ["విద్య", "జ్ఞానము"],
        "punya_left": "పుణ్యము", "punya_right": "పుణ్యము"
    },
    {
        "num": 6, "rasi": "కన్య", "color": "#06b6d4", "text_dark": True,
        "karakas": ["శత్రు, ఋణ", "రోగ"],
        "punya_left": "పుణ్యము", "punya_right": "పాపము"
    },
    {
        "num": 7, "rasi": "తుల", "color": "#18181b", "text_dark": False,
        "karakas": ["భార్య", "దేహ సుఖ"],
        "punya_left": "పాపము", "punya_right": "పాపము"
    },
    {
        "num": 8, "rasi": "వృశ్చికం", "color": "#ea580c", "text_dark": False,
        "karakas": ["ఆయుష్షు", "ప్రయాణములు"],
        "punya_left": "పాపము", "punya_right": "పుణ్యము"
    },
    {
        "num": 9, "rasi": "ధనుస్సు", "color": "#831843", "text_dark": False,
        "karakas": ["దానధర్మములు", "కీర్తి"],
        "punya_left": "పుణ్యము", "punya_right": "పుణ్యము"
    },
    {
        "num": 10, "rasi": "మకరం", "color": "#ffffff", "text_dark": True,
        "karakas": ["భక్తి, కర్మ"],
        "punya_left": "పుణ్యము", "punya_right": "పాపము"
    },
    {
        "num": 11, "rasi": "కుంభం", "color": "#9333ea", "text_dark": False,
        "karakas": ["విద్య అజ్ఞానము", "సంపద"],
        "punya_left": "పాపము", "punya_right": "పాపము"
    },
    {
        "num": 12, "rasi": "మీనం", "color": "#15803d", "text_dark": False,
        "karakas": ["మరణము", "మోక్షము"],
        "punya_left": "పాపము", "punya_right": "పుణ్యము"
    }
]

def pt(angle_deg, radius):
    rad = math.radians(angle_deg - 90)
    return cx + radius * math.cos(rad), cy + radius * math.sin(rad)

svg = []
svg.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" height="100%">
  <defs>
    <radialGradient id="bgGrad" cx="50%" cy="45%" r="65%">
      <stop offset="0%" stop-color="#15803d"/>
      <stop offset="70%" stop-color="#0f5c2b"/>
      <stop offset="100%" stop-color="#093d1b"/>
    </radialGradient>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#000" flood-opacity="0.45"/>
    </filter>
    <filter id="glowGold" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#fbbf24" flood-opacity="0.6"/>
    </filter>
  </defs>

  <style>
    .te-font {{
      font-family: 'Anek Telugu', 'Noto Serif Telugu', 'Ramabhadra', serif;
    }}
    .en-font {{
      font-family: 'Outfit', 'Segoe UI', Roboto, sans-serif;
    }}
  </style>

  <!-- Green Card Background -->
  <rect width="{W}" height="{H}" rx="28" fill="url(#bgGrad)"/>

  <!-- Top "శ్రీ" Symbol -->
  <g filter="url(#shadow)">
    <text x="{cx}" y="54" text-anchor="middle" class="te-font" font-size="48" font-weight="900" fill="#facc15" stroke="#78350f" stroke-width="1.8">శ్రీ</text>
  </g>

  <!-- Main Chakra Wheel Group -->
  <g filter="url(#shadow)">
    <!-- Outer rim -->
    <circle cx="{cx}" cy="{cy}" r="{r_outer}" fill="#0f172a" stroke="#000000" stroke-width="6"/>
''')

# Draw 12 Sectors
for s in sectors:
    i = s['num'] - 1
    a1 = i * 30
    a2 = (i + 1) * 30
    col = s['color']
    p1_x, p1_y = pt(a1, r_center)
    p2_x, p2_y = pt(a1, r_outer)
    p3_x, p3_y = pt(a2, r_outer)
    p4_x, p4_y = pt(a2, r_center)
    svg.append(f'''    <path d="M {p1_x:.2f} {p1_y:.2f} L {p2_x:.2f} {p2_y:.2f} A {r_outer} {r_outer} 0 0 1 {p3_x:.2f} {p3_y:.2f} L {p4_x:.2f} {p4_y:.2f} A {r_center} {r_center} 0 0 0 {p1_x:.2f} {p1_y:.2f} Z" fill="{col}" stroke="#000000" stroke-width="2"/>\n''')

# Concentric boundary rings
svg.append(f'''    <circle cx="{cx}" cy="{cy}" r="{r_inner}" fill="none" stroke="#000000" stroke-width="2"/>\n''')

# Sector Details: Rasi, Karakas, Brackets, Punya/Papa, House Number
for s in sectors:
    i = s['num'] - 1
    a1 = i * 30
    a2 = (i + 1) * 30
    amid = i * 30 + 15
    dark = s['text_dark']
    txt_col = '#0f172a' if dark else '#ffffff'
    bracket_col = '#ffffff' if not dark else '#1e293b'

    # 1. Rasi in outer ring (radius 335)
    rx, ry = pt(amid, 335)
    svg.append(f'''    <g transform="translate({rx:.2f}, {ry:.2f}) rotate({amid:.2f})">
      <text x="0" y="0" text-anchor="middle" dominant-baseline="central" class="te-font" font-size="22" font-weight="900" fill="{txt_col}">{s['rasi']}</text>
    </g>\n''')

    # 2. Punya / Papa along spokes (radius 338, angles a1+5.2 and a2-5.2)
    p_left = s['punya_left']
    p_right = s['punya_right']
    
    pl_x, pl_y = pt(a1 + 5.2, 338)
    svg.append(f'''    <g transform="translate({pl_x:.2f}, {pl_y:.2f}) rotate({a1 + 5.2:.2f})">
      <text x="0" y="0" text-anchor="middle" dominant-baseline="central" class="te-font" font-size="12" font-weight="800" fill="{txt_col}">{p_left}</text>
    </g>\n''')

    pr_x, pr_y = pt(a2 - 5.2, 338)
    svg.append(f'''    <g transform="translate({pr_x:.2f}, {pr_y:.2f}) rotate({a2 - 5.2:.2f})">
      <text x="0" y="0" text-anchor="middle" dominant-baseline="central" class="te-font" font-size="12" font-weight="800" fill="{txt_col}">{p_right}</text>
    </g>\n''')

    # 3. Ornate Bracket embracing Karakas (radius ~260, tip pointing outward to 274)
    b1_x, b1_y = pt(a1 + 1.5, 260)
    bm1_x, bm1_y = pt(amid - 4.5, 264)
    btip_x, btip_y = pt(amid, 274)
    bm2_x, bm2_y = pt(amid + 4.5, 264)
    b2_x, b2_y = pt(a2 - 1.5, 260)
    svg.append(f'''    <path d="M {b1_x:.2f} {b1_y:.2f} Q {bm1_x:.2f} {bm1_y:.2f} {btip_x:.2f} {btip_y:.2f} Q {bm2_x:.2f} {bm2_y:.2f} {b2_x:.2f} {b2_y:.2f}" fill="none" stroke="{bracket_col}" stroke-width="2.4" stroke-linecap="round"/>\n''')

    # 4. Karaka Text inside bracket (radius ~215)
    kx, ky = pt(amid, 215)
    karakas = s['karakas']
    svg.append(f'''    <g transform="translate({kx:.2f}, {ky:.2f}) rotate({amid:.2f})">\n''')
    if len(karakas) == 1:
        svg.append(f'''      <text x="0" y="0" text-anchor="middle" dominant-baseline="central" class="te-font" font-size="15.5" font-weight="800" fill="{txt_col}">{karakas[0]}</text>\n''')
    elif len(karakas) == 2:
        svg.append(f'''      <text x="0" y="-9" text-anchor="middle" dominant-baseline="central" class="te-font" font-size="14" font-weight="800" fill="{txt_col}">{karakas[0]}</text>
      <text x="0" y="11" text-anchor="middle" dominant-baseline="central" class="te-font" font-size="14" font-weight="800" fill="{txt_col}">{karakas[1]}</text>\n''')
    svg.append(f'''    </g>\n''')

    # 5. House Number (radius 138)
    nx, ny = pt(amid, 138)
    svg.append(f'''    <g transform="translate({nx:.2f}, {ny:.2f}) rotate({amid:.2f})">
      <text x="0" y="0" text-anchor="middle" dominant-baseline="central" class="te-font" font-size="22" font-weight="900" fill="{txt_col}">{s['num']}</text>
    </g>\n''')

# Center Core Circle: గురువు
svg.append(f'''    <circle cx="{cx}" cy="{cy}" r="{r_center}" fill="#ffffff" stroke="#000000" stroke-width="4.5"/>
    <text x="{cx}" y="{cy - 34}" text-anchor="middle" class="te-font" font-size="28" font-weight="900" fill="#1e3a8a">గు</text>
    <text x="{cx}" y="{cy + 3}" text-anchor="middle" class="te-font" font-size="34" font-weight="900" fill="#1e3a8a">గురువు</text>
    <text x="{cx}" y="{cy + 40}" text-anchor="middle" class="te-font" font-size="28" font-weight="900" fill="#1e3a8a">వు</text>
  </g>

  <!-- Bottom Title & Ornaments -->
  <g filter="url(#shadow)">
    <text x="{cx}" y="930" text-anchor="middle" class="te-font" font-size="38" font-weight="900" fill="#ff4081" stroke="#ffffff" stroke-width="1.8" filter="url(#glowGold)">కాల, కర్మ చక్రములు</text>
    <g stroke="#facc15" stroke-width="2" fill="none">
      <line x1="240" y1="952" x2="760" y2="952"/>
      <polygon points="500,946 506,952 500,958 494,952" fill="#facc15"/>
      <polygon points="484,948 488,952 484,956 480,952" fill="#facc15"/>
      <polygon points="516,948 520,952 516,956 512,952" fill="#facc15"/>
      <path d="M 240 952 C 220 942, 200 962, 180 947" stroke="#facc15" stroke-width="2.5"/>
      <path d="M 760 952 C 780 942, 800 962, 820 947" stroke="#facc15" stroke-width="2.5"/>
    </g>
    <text x="{cx}" y="985" text-anchor="middle" class="en-font" font-size="18" font-weight="700" fill="#ffffff" letter-spacing="0.5">Author : The Only Guru of Three Religions</text>
    <text x="{cx}" y="1015" text-anchor="middle" class="en-font" font-size="16" font-weight="600" fill="#fef08a" letter-spacing="0.5">The Spiritual Emperor Thraitha Thought Originator</text>
    <text x="{cx}" y="1045" text-anchor="middle" class="te-font" font-size="14.5" font-weight="700" fill="#e2e8f0" opacity="0.95">ద్వాదశ గ్రహ జ్యోతిష శాస్త్రవేత్త, ఆధ్యాత్మిక సామ్రాజ్య చక్రవర్తి శ్రీశ్రీశ్రీ ఆచార్య ప్రబోధానంద భగవానులు</text>
  </g>
</svg>
''')

svg_str = ''.join(svg)
svg_p = os.path.join(out_dir, "thraitha_chakra_8k.svg")
with open(svg_p, "w", encoding="utf-8") as f:
    f.write(svg_str)
print("Generated new SVG, size:", len(svg_str))

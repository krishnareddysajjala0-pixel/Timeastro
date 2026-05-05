import os

APP_FILE = "app.py"
PANCHANGAM_FILE = "templates/panchangam.html"
DAILY_FILE = "templates/daily_panchangam.html"
CALENDAR_FILE = "templates/calendar_view.html"

# 1. Update app.py to return chart in daily_panchangam
with open(APP_FILE, "r", encoding="utf-8") as f:
    app_content = f.read()

if "planet_positions, chart_data, lagna_houses" not in app_content:
    replacement = """
    panch_data = get_daily_panchangam_basic(jd, lat, lon, local_tz, local_midnight, calc_end_times=True)
    
    try:
        from app import chart
        # The logic is deeply embedded in chart(). We only want the array parts.
        # It's better to just re-implement the short calculation here:
        import swisseph as swe
        
        PLANETS = {
            "సూర్యుడు": swe.SUN, "చంద్రుడు": swe.MOON, "కుజుడు": swe.MARS,
            "బుధ": swe.MERCURY, "గురు": swe.JUPITER, "శుక్ర": swe.VENUS, "శని": swe.SATURN
        }
        LAGNA_NAMES_TELUGU = ["మేషం", "వృషభం", "మిథునం", "కర్కాటకం", "సింహం", "కన్య", "తులా", "వృశ్చికం", "ధనస్సు", "మకరం", "కుంభం", "మీనం"]
        
        chart_data_temp = {r:[] for r in LAGNA_NAMES_TELUGU}
        base_pos = {}
        for name_p, pid in PLANETS.items():
            lonp = swe.calc_ut(jd, pid, 2|256)[0][0]
            base_pos[name_p] = lonp
            r = LAGNA_NAMES_TELUGU[int(lonp/30)]
            d = int(lonp%30); m = int(((lonp%30)-d)*60)
            chart_data_temp[r].append((lonp%30, f"<b>{name_p}</b> <small>{d}°{m:02d}′</small>"))
            
        rahu = base_pos.get("రాహు", 0)
        ketu = (rahu + 180) % 360
        r = LAGNA_NAMES_TELUGU[int(ketu/30)]
        d = int(ketu%30); m = int(((ketu%30)-d)*60)
        chart_data_temp[r].append((ketu%30, f"<b>కేతు</b> <small>{d}°{m:02d}′</small>"))
        base_pos["కేతు"] = ketu
        
        der = {"భూమి": (base_pos.get("సూర్యుడు", 0)+180)%360, "చిత్ర": (rahu+3.3333)%360, "మిత్ర": (ketu+3.3333)%360}
        for n, lonp in der.items():
            r = LAGNA_NAMES_TELUGU[int(lonp/30)]
            d = int(lonp%30); m = int(((lonp%30)-d)*60)
            chart_data_temp[r].append((lonp%30, f"<b>{n}</b> <small>{d}°{m:02d}′</small>"))
            
        # hands
        for n, base in base_pos.items():
            hl = (base + 180)%360
            r = LAGNA_NAMES_TELUGU[int(hl/30)]
            d = int(hl%30); min_val = int(((hl%30)-d)*60)
            chart_data_temp[r].append((hl%30, f"<span class='hand'><span style='font-size: 0.7em;'>👉</span> {n} <small>{d}°{min_val:02d}′</small></span>"))
            
        hus, ascmc = swe.houses(jd, lat, lon)
        lagna_lon = (ascmc[0] - swe.get_ayanamsa_ut(jd)) % 360
        lagna = LAGNA_NAMES_TELUGU[int(lagna_lon/30)]
        lagna_deg = int(lagna_lon%30); lagna_min = int(((lagna_lon%30)-lagna_deg)*60)
        chart_data_temp[lagna].append((lagna_lon%30, f"<b>లగ్నం</b> <small>{lagna_deg}°{lagna_min:02d}′</small>"))
        
        chart_data = {r: '<br>'.join([x[1] for x in sorted(lst, key=lambda i: i[0])]) for r,lst in chart_data_temp.items()}
        lgn_idx = LAGNA_NAMES_TELUGU.index(lagna)
        lagna_houses = {LAGNA_NAMES_TELUGU[(lgn_idx + i) % 12]: i+1 for i in range(12)}
        
        panch_data['chart'] = chart_data
        panch_data['houses'] = lagna_houses
        panch_data['lagna'] = lagna
    except Exception as e:
        print("Error computing chart for daily panchangam", e)
"""
    app_content = app_content.replace(
        "panch_data = get_daily_panchangam_basic(jd, lat, lon, local_tz, local_midnight, calc_end_times=True)",
        replacement
    )
    with open(APP_FILE, "w", encoding="utf-8") as f:
        f.write(app_content)


# 2. Remove Grid from panchangam.html
with open(PANCHANGAM_FILE, "r", encoding="utf-8") as f:
    p_content = f.read()

import re
p_content = re.sub(r'<h2 class="section-title">.*?<i class="fas fa-th-large section-icon"></i> కుండలి \(Kundali Grid\).*?</div>\s*</div>', '', p_content, flags=re.DOTALL)
with open(PANCHANGAM_FILE, "w", encoding="utf-8") as f:
    f.write(p_content)


# 3. Add Full Grid and loading spinner to daily_panchangam.html
with open(DAILY_FILE, "r", encoding="utf-8") as f:
    d_content = f.read()

d_content = d_content.replace('<form action="/daily_panchangam" method="POST">', '<form action="/daily_panchangam" method="POST" onsubmit="showLoading()">')

chart_html = """
                <!-- Planet Grid -->
                <style>
                .chart-container-c { margin: 30px auto 10px; padding: 15px; background: rgba(0, 0, 0, 0.2); border-radius: 20px; border: 1px solid rgba(255,255,255,0.15); width: 100%; overflow-x: auto; }
                .chart-c { display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, minmax(80px, auto)); gap: 5px; width: 100%; min-width: 300px; }
                .box-c { position: relative; border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 5px; padding: 5px; background: rgba(255, 255, 255, 0.03); font-size: 11px; }
                .lagna-c { border: 2px solid gold; box-shadow: 0 0 10px rgba(255, 215, 0, 0.3); }
                .house-no-c { position: absolute; top: 2px; right: 2px; background: rgba(0,0,0,0.5); width: 15px; height: 15px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 9px; font-weight: bold; color: #a0a0ff; }
                .lagna-name-c { position: absolute; bottom: 2px; right: 2px; background: rgba(0,0,0,0.5); padding: 1px 4px; border-radius: 4px; font-size: 9px; color: #f8fafc; opacity: 0.7; }
                .center-c { grid-column: 2 / 4; grid-row: 2 / 4; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255,255,255,0.15); border-radius: 8px; font-size: 14px; font-weight: bold; background: rgba(0,0,0,0.1); color: #ffd700; text-align: center; }
                .hand { display: inline-block; padding: 1px 4px; border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; margin: 1px 0; background: rgba(255,255,255,0.05); }
                </style>
                
                {% if panch.chart %}
                <h2 class="section-title"><i class="fas fa-th-large section-icon"></i> లగ్న చక్రం</h2>
                {% macro full_box(lagna) %}
                    {% set hno = panch.houses.get(lagna, "") if panch.houses else "" %}
                    <div class="box-c {% if panch.lagna==lagna %}lagna-c{% endif %}">
                        {% if hno %}<span class="house-no-c">{{ hno }}</span>{% endif %}
                        <div style="margin-bottom: 12px; line-height: 1.4;">{{ panch.chart[lagna] | safe }}</div>
                        <span class="lagna-name-c">{{ lagna }}</span>
                    </div>
                {% endmacro %}
                <div class="chart-container-c">
                    <div class="chart-c">
                        {{ full_box("మీనం") }} {{ full_box("మేషం") }} {{ full_box("వృషభం") }} {{ full_box("మిథునం") }}
                        {{ full_box("కుంభం") }} <div class="center-c">జాఫతకము</div> {{ full_box("కర్కాటకం") }}
                        {{ full_box("మకరం") }} {{ full_box("సింహం") }}
                        {{ full_box("ధనస్సు") }} {{ full_box("వృశ్చికం") }} {{ full_box("తులా") }} {{ full_box("కన్య") }}
                    </div>
                </div>
                {% endif %}
"""
if "లగ్న చక్రం" not in d_content:
    d_content = d_content.replace('</div>\n    </div>\n\n    <!-- Navigation Buttons -->', f'{chart_html}</div>\n    </div>\n\n    <!-- Navigation Buttons -->')

loading_css_js = """
<style>
.loading { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15,12,41,0.9); display: none; flex-direction: column; justify-content: center; align-items: center; z-index: 999999; backdrop-filter: blur(5px); }
.spinner { width: 50px; height: 50px; border: 5px solid rgba(255, 215, 0, 0.3); border-top-color: #ffd700; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 20px; }
@keyframes spin { to { transform: rotate(360deg); } }
.loading-text { color: #ffd700; font-size: 20px; font-weight: bold; text-shadow: 0 0 10px rgba(255, 215, 0, 0.5); }
</style>
<div class="loading" id="loading"><div class="spinner"></div><div class="loading-text">జరగబోయేది నీవు తెలుసుకున్న తెలుసుకోకున్నా ఏది జరగాలో అదే జరిగి తీరుతుంది.</div></div>
<script>
function showLoading() { document.getElementById('loading').style.display = 'flex'; }
function hideLoading() { document.getElementById('loading').style.display = 'none'; }
window.addEventListener('pageshow', function (e) { hideLoading(); });
</script>
"""
if 'id="loading"' not in d_content:
    d_content = d_content.replace('<body>', f'<body>{loading_css_js}')

with open(DAILY_FILE, "w", encoding="utf-8") as f:
    f.write(d_content)


# 4. Add Loading spinner to calendar_view.html
with open(CALENDAR_FILE, "r", encoding="utf-8") as f:
    c_content = f.read()

c_content = c_content.replace('<form method="POST" action="/calendar_view">', '<form method="POST" action="/calendar_view" onsubmit="showLoading()">')
if 'id="loading"' not in c_content:
    c_content = c_content.replace('<body>', f'<body>{loading_css_js}')

with open(CALENDAR_FILE, "w", encoding="utf-8") as f:
    f.write(c_content)

print("Done modifications!")

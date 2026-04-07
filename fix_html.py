import re

with open('templates/daily_panchangam.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I will cleanly wipe ANY macro full_box and chart-c code, and re-insert it properly!
html = re.sub(r'{% if panch\.chart %}.*?{% endif %}', '', html, flags=re.DOTALL)
# maybe the tags are isolated
html = re.sub(r'{% macro full_box.*?{% endmacro %}', '', html, flags=re.DOTALL)
html = re.sub(r'<div class="chart-container-c">.*?</div>\s*</div>\s*', '', html, flags=re.DOTALL)
html = html.replace('<h2 class="section-title"><i class="fas fa-th-large section-icon"></i> రాశి చక్రం</h2>', '')

chart_block = """
                {% if panch.chart %}
                <h2 class="section-title" style="margin-top: 20px;"><i class="fas fa-th-large section-icon"></i> రాశి చక్రం</h2>
                {% macro full_box(rasi, panch) %}
                    {% set hno = panch.houses.get(rasi, "") if panch.houses else "" %}
                    <div class="box-c {% if panch.lagna==rasi %}lagna-c{% endif %}">
                        {% if hno %}<span class="house-no-c">{{ hno }}</span>{% endif %}
                        <div style="margin-bottom: 12px; line-height: 1.4;">{{ panch.chart[rasi] | safe }}</div>
                        <span class="rasi-name-c">{{ rasi }}</span>
                    </div>
                {% endmacro %}
                <div class="chart-container-c">
                    <div class="chart-c">
                        {{ full_box("మీనం", panch) }} {{ full_box("మేషం", panch) }} {{ full_box("వృషభం", panch) }} {{ full_box("మిథునం", panch) }}
                        {{ full_box("కుంభం", panch) }} <div class="center-c">జాతకము</div> {{ full_box("కర్కాటకం", panch) }}
                        {{ full_box("మకరం", panch) }} {{ full_box("సింహం", panch) }}
                        {{ full_box("ధనస్సు", panch) }} {{ full_box("వృశ్చికం", panch) }} {{ full_box("తులా", panch) }} {{ full_box("కన్య", panch) }}
                    </div>
                </div>
                {% endif %}
"""

# Now inject chart_block after "ચంద్రోదయం & ચంద్రాస్తమయం" result-item
html = html.replace('<!-- Tithi -->', chart_block + '\n                <!-- Tithi -->')

with open('templates/daily_panchangam.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("HTML successfully fixed!")

import sys

# Get CSS and base structure from compare_results.html
with open('templates/compare_results.html', 'r', encoding='utf-8') as f:
    compare_res = f.read()

# Get Dasa styling and content from chart2.html
with open('templates/chart2.html', 'r', encoding='utf-8') as f:
    chart2 = f.read()

# Build the new template
head_start = compare_res.find('<head>')
head_end = compare_res.find('</head>')

# Extract chart2 CSS 
# Because chart2 has complex CSS for printing and dasa styling, we just take all its CSS
c2_style_start = chart2.find('<style>')
c2_style_end = chart2.find('</style>')
c2_css = chart2[c2_style_start+7:c2_style_end] if c2_style_start != -1 else ''

# Extract body block for Dasa from chart2
c2_content_start = chart2.find('<div class="glow-container"')
if c2_content_start == -1:
    c2_content_start = chart2.find('<div class="dasa-section"')

c2_content_end = chart2.find('<div id="transit-container">')
if c2_content_end == -1:
    c2_content_end = chart2.find('<div class="fixed-bottom-bar">')
if c2_content_end == -1:
    c2_content_end = chart2.find('</body>')

dasa_block = chart2[c2_content_start:c2_content_end]

# We need to replace variables in dasa_block to namespace them for dasha1 and dasha2
def namespace_vars(block, prefix, dasa_prefix):
    # Variables that are part of birth_info: name, dob, tob, etc.
    block = block.replace('{{ name }}', '{{ ' + prefix + '.name }}')
    block = block.replace('{{ dob }}', '{{ ' + prefix + '.dob }}')
    block = block.replace('{{ tob }}', '{{ ' + prefix + '.tob }}')
    block = block.replace('{{ place }}', '{{ ' + prefix + '.place }}')
    block = block.replace('{{ nakshatra }}', '{{ ' + prefix + '.nakshatra }}')
    block = block.replace('{{ padam }}', '{{ ' + prefix + '.padam }}')
    block = block.replace('{{ nak_elapsed }}', '{{ ' + prefix + '.nak_elapsed }}')
    block = block.replace('{{ nak_remaining }}', '{{ ' + prefix + '.nak_remaining }}')
    
    # Variables that belong to the new dasha dict
    # maha, maha_start, maha_end, etc.
    dasa_vars = ['maha', 'maha_start', 'maha_end', 'maha_age_start', 'maha_age_end',
                 'total_years', 'completed_years', 'remaining_years',
                 'current_dasa_color', 'current_dasa_icon', 'current_dasa_favorable',
                 'total_cycle_years', 'all_dasas']
    for v in dasa_vars:
        block = block.replace('{{ ' + v + ' ', '{{ ' + dasa_prefix + '.' + v + ' ')
        block = block.replace('{{ ' + v + '}}', '{{ ' + dasa_prefix + '.' + v + '}}')
        block = block.replace('{{' + v + '}}', '{{' + dasa_prefix + '.' + v + '}}')
        
    # the for loop: {% for dasa in all_dasas %} -> {% for dasa in dashaX.all_dasas %}
    block = block.replace('{% for dasa in all_dasas %}', '{% for dasa in ' + dasa_prefix + '.all_dasas %}')

    # the onclick: toggleAccordion -> toggleAccordionX depending on prefix so they don't break each other
    block = block.replace('id="maha-{{ loop.index }}"', 'id="maha-' + prefix + '-{{ loop.index }}"')
    block = block.replace("toggleAccordion('maha-{{ loop.index }}')", "toggleAccordion('maha-" + prefix + "-{{ loop.index }}')")

    return block

block1 = namespace_vars(dasa_block, 'p1', 'dasha1')
block2 = namespace_vars(dasa_block, 'p2', 'dasha2')

new_html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>దశాచార పోలిక</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
{compare_res[compare_res.find('<style>')+7:compare_res.find('</style>')]}
/* chart2 CSS */
{c2_css}

/* Ensure compare wrapping still works */
.compare-wrapper {{
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 100%;
    max-width: 1800px;
    margin: 0 auto;
    padding: 0 20px;
}}
@media (min-width: 1100px) {{
    .compare-wrapper {{
        flex-direction: row;
    }}
    .chart-container-wrapper {{
        flex: 1;
        min-width: 0;
    }}
}}

    </style>
</head>
<body class="dark-mode">
  <div class="header" style="margin-top: 20px;">
    <h2 class="page-title">దశాచార పోలిక</h2>
  </div>

  <button onclick="window.history.back()" class="btn print-hide" style="position: fixed; top: 20px; left: 20px; z-index: 10000; background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; padding: 8px 16px; border-radius: 8px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.3); font-size: 14px;"><i class="fas fa-arrow-left"></i> వెనుకకు</button>
  <button onclick="window.print()" class="btn print-hide" style="position: fixed; top: 20px; right: 20px; z-index: 10000; background: linear-gradient(135deg, #e91e63, #c2185b); color: white; padding: 8px 16px; border-radius: 8px; border: none; cursor: pointer; display: flex; align-items: center; gap: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);"><i class="fas fa-print"></i> ప్రింట్</button>

  <div class="compare-wrapper">
    <div class="chart-container-wrapper">
      <div class="compare-person-header">{{{{ p1.name }}}}</div>
      {block1}
    </div>
    
    <div class="chart-container-wrapper">
      <div class="compare-person-header">{{{{ p2.name }}}}</div>
      {block2}
    </div>
  </div>

  <div id="loading-overlay">
      <div class="loader-astro"></div>
      <p style="font-size: 20px; font-weight: bold;">జరగబోయేది నీవు తెలుసుకున్న తెలుసుకోకున్నా ఏది జరగాలో అదే జరిగి తీరుతుంది.</p>
  </div>
  
  <!-- Same bottom bar as compare_results -->
  <div class="fixed-bottom-bar-nav">
      <a href="/" class="nav-item nav-home">
          <i class="fas fa-home"></i>
          <span>హోమ్</span>
      </a>
      <a href="/compare_kundali" class="nav-item active nav-compare">
          <i class="fas fa-balance-scale"></i>
          <span>పోలిక</span>
      </a>
      <a href="/daily_panchangam" class="nav-item nav-panch">
          <i class="fas fa-om"></i>
          <span>దిన పంచాంగం</span>
      </a>
      <a href="/calendar_view" class="nav-item nav-cal">
          <i class="fas fa-calendar-alt"></i>
          <span>క్యాలెండర్</span>
      </a>
  </div>
  
  <script>
      function toggleAccordion(id) {{
          var content = document.getElementById(id);
          var header = content.previousElementSibling;
          
          if (content.style.maxHeight) {{
              content.style.maxHeight = null;
              content.style.opacity = '0';
              content.style.visibility = 'hidden';
              content.style.marginTop = '0';
              header.classList.remove('active');
          }} else {{
              content.style.maxHeight = content.scrollHeight + "px";
              content.style.opacity = '1';
              content.style.visibility = 'visible';
              content.style.marginTop = '15px';
              header.classList.add('active');
          }}
      }}
      
      function showLoader() {{
          document.getElementById('loading-overlay').style.display = 'flex';
      }}
      document.querySelectorAll('.nav-item').forEach(item => {{
          item.addEventListener('click', function(e) {{
              if(!this.href.includes('#')) showLoader();
          }});
      }});
  </script>
</body>
</html>
"""

with open('templates/compare_dasha.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Generated compare_dasha.html")

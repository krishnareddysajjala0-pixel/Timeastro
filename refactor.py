import sys

app_path = 'app.py'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

start_chart2 = content.find('@app.route("/chart2")')
if start_chart2 == -1:
    start_chart2 = content.find('@app.route("/chart2", methods=["GET", "POST"])')

end_chart2 = content.find('@app.route("/chart3")', start_chart2)

with open('scratch.py', 'r', encoding='utf-8') as f:
    scratch = f.read()

logic_start = scratch.find('    dob = birth_info')
logic_end = scratch.rfind('    return render_template(')

logic_body = scratch[logic_start:logic_end]

helper_func = """def get_dasha_info(birth_info):
""" + logic_body + """
    return {
        "maha": current_maha_name,
        "maha_start": current_maha_start,
        "maha_end": current_maha_end,
        "maha_age_start": current_maha_age_start,
        "maha_age_end": current_maha_age_end,
        "total_years": current_maha_years,
        "completed_years": round(elapsed_years_current, 2),
        "remaining_years": round(remaining_years_current, 2),
        "current_dasa_color": current_dasa_color,
        "current_dasa_icon": current_dasa_icon,
        "current_dasa_favorable": current_dasa_favorable,
        "all_dasas": all_dasas,
        "total_cycle_years": total_years_covered,
    }

"""

new_chart2 = """@app.route("/chart2", methods=["GET", "POST"])
def chart2():
    birth_info = session.get('birth_info', {})
    
    dob = birth_info.get('dob', '')
    tob = birth_info.get('tob', '')
    name = birth_info.get('name', '')
    place = birth_info.get('place', '')
    day_name = birth_info.get('day_name', '')
    nakshatra = birth_info.get('nakshatra', '')
    padam = birth_info.get('padam', 1)
    nak_elapsed = birth_info.get('nak_elapsed', '0గం 0ని')
    nak_remaining = birth_info.get('nak_remaining', '0గం 0ని')

    if not dob:
        return "❌ No birth info found"

    dasha_data = get_dasha_info(birth_info)

    return render_template(
        "chart2.html",
        name=name, dob=dob, tob=tob, place=place, day_name=day_name,
        nakshatra=nakshatra, padam=padam, nak_elapsed=nak_elapsed, nak_remaining=nak_remaining,
        **dasha_data,
        planet_colors=PLANET_COLORS,
    )

"""

compare_dasha_route = """
@app.route("/compare_dasha", methods=["POST"])
def compare_dasha():
    name1 = request.form.get("name1","")
    dob1 = request.form.get("dob1","")
    tob1 = request.form.get("tob1","")
    place1 = request.form.get("place1","")
    lat1 = request.form.get("lat1")
    lon1 = request.form.get("lon1")

    name2 = request.form.get("name2","")
    dob2 = request.form.get("dob2","")
    tob2 = request.form.get("tob2","")
    place2 = request.form.get("place2","")
    lat2 = request.form.get("lat2")
    lon2 = request.form.get("lon2")

    if not lat1 or not lon1 or not lat2 or not lon2:
        return "❌ Please select place from suggestion list for both entries"

    data1 = get_kundali_data(name1, dob1, tob1, place1, float(lat1), float(lon1))
    data2 = get_kundali_data(name2, dob2, tob2, place2, float(lat2), float(lon2))
    
    dasha1 = get_dasha_info(data1)
    dasha2 = get_dasha_info(data2)

    return render_template("compare_dasha.html", p1=data1, p2=data2, dasha1=dasha1, dasha2=dasha2, planet_colors=PLANET_COLORS)

"""

content = content[:start_chart2] + helper_func + new_chart2 + compare_dasha_route + content[end_chart2:]

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Refactored app.py')

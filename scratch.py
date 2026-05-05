def chart2():
    # Get birth info from session
    birth_info = session.get('birth_info', {})
    # Extract values
    dob = birth_info.get('dob', '')
    tob = birth_info.get('tob', '')
    name = birth_info.get('name', '')
    place = birth_info.get('place', '')
    day_name = birth_info.get('day_name', '')
    nakshatra = birth_info.get('nakshatra', '')
    lagna = birth_info.get('lagna', '')
    nak_elapsed = birth_info.get('nak_elapsed', '0గం 0ని')
    nak_remaining = birth_info.get('nak_remaining', '0గం 0ని')
    nak_index = birth_info.get('nak_index', 0)
    elapsed_h = birth_info.get('elapsed_h', 0)
    elapsed_m = birth_info.get('elapsed_m', 0)
    padam = birth_info.get('padam', 1)

    # Parse birth datetime
    timezone_str = birth_info.get('timezone_str', 'Asia/Kolkata')
    local_tz = pytz.timezone(timezone_str)
    try:
        birth_dt = local_tz.localize(
            datetime.datetime.strptime(dob + " " + tob, "%Y-%m-%d %H:%M")
        )
    except ValueError:
        return "❌ Invalid date/time format"

    # ===== CALCULATE FULL 120-YEAR DASA CYCLE =====
    
    # 1. Calculate birth Mahadasha
    birth_dasa, dasa_index = get_running_dasa(nak_index, padam)
    
    # 2. Calculate elapsed time in birth dasa (Based on Rasi-based 30-degree movement)
    moon_lon = birth_info.get('moon_lon')
    if moon_lon is None:
        # Fallback to manual timing if longitude not stored
        elapsed_minutes = nak_minutes(elapsed_h, elapsed_m)
        fraction = elapsed_minutes / TOTAL_NAK_MINUTES if TOTAL_NAK_MINUTES > 0 else 0
    else:
        # According to the text, each Dasa is 30 degrees (9 padas/1 Rasi)
        fraction = (moon_lon % 30) / 30
    
    birth_dasa_years = DASA_YEARS.get(birth_dasa, 10)
    elapsed_years_in_birth_dasa = birth_dasa_years * fraction
    
    # 3. Calculate start date of birth dasa (before birth)
    birth_dasa_start = birth_dt - datetime.timedelta(days=int(elapsed_years_in_birth_dasa * 365.25))
    birth_dasa_end = add_years(birth_dasa_start, birth_dasa_years)
    
    # 4. Get today's date for current dasa detection
    today = datetime.datetime.now()
    today_str = today.strftime("%d-%m-%Y")
    
    # 5. Calculate ALL 12 Mahadashas in sequence (120 years)
    all_dasas = []
    start_date = birth_dasa_start
    
    # Variables to track current dasa
    current_maha_index = -1
    current_maha_name = ""
    current_maha_start = ""
    current_maha_end = ""
    current_maha_years = 0
    current_maha_age_start = ""
    current_maha_age_end = ""
    
    # Start from birth dasa and go through all 12
    for i in range(12):
        dasa_index_calc = (dasa_index + i) % 12
        dasa_name = DASA_ORDER[dasa_index_calc]
        dasa_years = DASA_YEARS.get(dasa_name, 10)
        
        end_date = add_years(start_date, dasa_years)
        start_str = start_date.strftime("%d-%m-%Y")
        end_str = end_date.strftime("%d-%m-%Y")
        
        # Calculate Anthara dasas for this Mahadasha
        antharas = calculate_anthara_periods(dasa_name, start_date, end_date, lagna, birth_dt)
        
        # Check if TODAY is within this dasa
        is_current_today = is_date_within_range(today_str, start_str, end_str)
        
        # Check if this is the birth dasa
        is_birth_dasa = (i == 0)
        
        # Determine favorability for full Mahadasa
        is_maha_favorable = is_dasa_favorable(lagna, dasa_name)
        
        # Add color and icon to dasa
        dasa_color = "#22c55e" if is_maha_favorable else "#ef4444"
        dasa_icon = PLANET_ICONS.get(dasa_name, "•")
        
        
        # Calculate Age
        age_start_str = ""
        age_end_str = ""
        
        age_start_days = (start_date - birth_dt).days
        if age_start_days >= 0:
            age_start_y = age_start_days // 365
            age_start_m = (age_start_days % 365) // 30
            age_start_str = f"{age_start_y}సం, {age_start_m}నెలలు"
            
        age_end_days = (end_date - birth_dt).days
        if age_end_days >= 0:
            age_end_y = age_end_days // 365
            age_end_m = (age_end_days % 365) // 30
            age_end_str = f"{age_end_y}సం, {age_end_m}నెలలు"

        # Add this Mahadasha to list
        all_dasas.append({
            "maha": dasa_name,
            "start": start_str,
            "end": end_str,
            "years": dasa_years,
            "antharas": antharas,
            "is_current": is_current_today,
            "is_birth_dasa": is_birth_dasa,
            "color": dasa_color,
            "icon": dasa_icon,
            "is_favorable": is_maha_favorable,
            "age_start": age_start_str,
            "age_end": age_end_str
        })
        
        # If this is current dasa, store its info
        if is_current_today:
            current_maha_index = i
            current_maha_name = dasa_name
            current_maha_start = start_str
            current_maha_end = end_str
            current_maha_years = dasa_years
            current_maha_age_start = age_start_str
            current_maha_age_end = age_end_str
        
        # Move to next Mahadasha start date
        start_date = end_date
    
    # 6. If no dasa matches today, use birth dasa as current
    if current_maha_index == -1:
        today_dt = datetime.datetime.strptime(today_str, "%d-%m-%Y")
        birth_start_dt = datetime.datetime.strptime(birth_dasa_start.strftime("%d-%m-%Y"), "%d-%m-%Y")
        
        if today_dt < birth_start_dt:
            current_maha_index = 0
        else:
            current_maha_index = 11
        
        current_maha_name = all_dasas[current_maha_index]["maha"]
        current_maha_start = all_dasas[current_maha_index]["start"]
        current_maha_end = all_dasas[current_maha_index]["end"]
        current_maha_years = all_dasas[current_maha_index]["years"]
        current_dasa_favorable = all_dasas[current_maha_index]["is_favorable"]
        current_maha_age_start = all_dasas[current_maha_index].get("age_start", "")
        current_maha_age_end = all_dasas[current_maha_index].get("age_end", "")
    else:
        current_dasa_favorable = is_dasa_favorable(lagna, current_maha_name)
    
    # 7. Calculate elapsed/remaining for CURRENT dasa
    current_start_dt = datetime.datetime.strptime(current_maha_start, "%d-%m-%Y")
    current_end_dt = datetime.datetime.strptime(current_maha_end, "%d-%m-%Y")
    
    # Calculate elapsed days in current dasa
    total_days_current = (current_end_dt - current_start_dt).days
    elapsed_days_current = (today - current_start_dt).days
    
    # Ensure days are within range
    elapsed_days_current = max(0, min(elapsed_days_current, total_days_current))
    
    elapsed_years_current = elapsed_days_current / 365.25
    remaining_years_current = (total_days_current - elapsed_days_current) / 365.25
    
    # 8. Calculate total years covered
    total_years_covered = sum(dasa.get("years", 10) for dasa in all_dasas)
    
    # 9. Current year for reference
    current_year = datetime.datetime.now().year
    
    # 10. Get planet colors and icons for current dasa
    current_dasa_color = PLANET_COLORS.get(current_maha_name, "#FFD700")
    current_dasa_icon = PLANET_ICONS.get(current_maha_name, "☉")

    
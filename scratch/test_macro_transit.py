import swisseph as swe
import datetime
import pytz

swe.set_sid_mode(swe.SIDM_LAHIRI)
PLANET_FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

def get_planet_lon(jd_val, pid):
    return swe.calc_ut(jd_val, pid, PLANET_FLAGS)[0][0]

def find_macro_boundary(jd_start, name, pid, current_lagna_idx, find_exit, max_days=10950):
    direction = 1 if find_exit else -1
    step = 15 if name == "Guru" else 2
    is_retro_planet = False
    
    if not find_exit:
        expected_lagna_b = (current_lagna_idx - 1) % 12 if not is_retro_planet else (current_lagna_idx + 1) % 12
    else:
        expected_lagna_b = (current_lagna_idx + 1) % 12 if not is_retro_planet else (current_lagna_idx - 1) % 12

    jd_a = jd_start
    for _ in range(int(max_days / step) + 2):
        jd_b = jd_a + direction * step
        lon_b = get_planet_lon(jd_b, pid)
        lagna_b = int(lon_b / 30) % 12
        
        # Only perform binary search if the lagna changed to the EXPECTED lagna
        if lagna_b != current_lagna_idx:
            if lagna_b == expected_lagna_b:
                lo, hi = min(jd_a, jd_b), max(jd_a, jd_b)
                for _ in range(35):
                    mid = (lo + hi) / 2
                    lon_mid = get_planet_lon(mid, pid)
                    lagna_mid = int(lon_mid / 30) % 12
                    
                    if lagna_mid == current_lagna_idx:
                        if direction > 0: lo = mid
                        else: hi = mid
                    else:
                        if direction > 0: hi = mid
                        else: lo = mid
                return hi if direction > 0 else lo
            else:
                # It changed to an unexpected lagna (e.g. retrograde back into same sign). 
                # We update jd_a but we DON'T return. We keep searching.
                pass
        jd_a = jd_b
    return None

jd = swe.julday(2026,4,15)
lon = get_planet_lon(jd, swe.JUPITER)
curr_idx = int(lon/30)%12

entry = find_macro_boundary(jd, "Guru", swe.JUPITER, curr_idx, False)
exit_jd = find_macro_boundary(jd, "Guru", swe.JUPITER, curr_idx, True)

def fmt(j):
    y,m,d,h = swe.revjul(j)
    dt = datetime.datetime(int(y),int(m),int(d)) + datetime.timedelta(hours=h)
    return pytz.utc.localize(dt).astimezone(pytz.timezone('Asia/Kolkata')).strftime("%Y-%m-%d")

print(f"Guru (Mithuna) Entry: {fmt(entry)}, Exit: {fmt(exit_jd)}")

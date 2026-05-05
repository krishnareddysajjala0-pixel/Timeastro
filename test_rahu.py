import swisseph as swe, pytz, datetime

swe.set_sid_mode(swe.SIDM_LAHIRI)
PLANET_FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
local_tz = pytz.timezone('Asia/Kolkata')
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

jd_now = swe.julday(2026, 4, 15, 4.0)

def get_rahu_lon(jd_val):
    return swe.calc_ut(jd_val, swe.MEAN_NODE, PLANET_FLAGS)[0][0]

def fmt(jd_val):
    y, m, d, h = swe.revjul(jd_val)
    dt = datetime.datetime(int(y), int(m), int(d), int(h), int((h % 1) * 60))
    dt = pytz.utc.localize(dt).astimezone(local_tz)
    return f'{dt.day} {months[dt.month-1]} {dt.year} {dt.strftime("%H:%M")} IST'

r_lon = get_rahu_lon(jd_now)
lagna_idx = int(r_lon / 30) % 12
print(f'Rahu lon: {r_lon:.4f} -> lagna index {lagna_idx} (Kumbha=10)')

step = 15

# bound1: find_exit=True -> direction = -1 (retro planet goes backward in time to find exit)
jd_a = jd_now
bound1 = None
for _ in range(120):
    jd_b = jd_a + (-1) * step
    lon_b = get_rahu_lon(jd_b)
    if int(lon_b / 30) % 12 != lagna_idx:
        lo, hi = min(jd_a, jd_b), max(jd_a, jd_b)
        for _ in range(35):
            mid = (lo + hi) / 2
            if int(get_rahu_lon(mid) / 30) % 12 == lagna_idx:
                hi = mid  # direction=-1, keep the side closer to jd_a (higher JD)
            else:
                lo = mid
        bound1 = hi
        break
    jd_a = jd_b

# bound2: find_exit=False -> direction = +1 (retro planet goes forward in time to find entry)
jd_a = jd_now
bound2 = None
for _ in range(120):
    jd_b = jd_a + (+1) * step
    lon_b = get_rahu_lon(jd_b)
    if int(lon_b / 30) % 12 != lagna_idx:
        lo, hi = min(jd_a, jd_b), max(jd_a, jd_b)
        for _ in range(35):
            mid = (lo + hi) / 2
            if int(get_rahu_lon(mid) / 30) % 12 == lagna_idx:
                lo = mid  # direction=+1, keep the side closer to jd_a (lower JD)
            else:
                hi = mid
        bound2 = lo
        break
    jd_a = jd_b

print(f'bound1 (time-backward for retro exit): {fmt(bound1)} JD={bound1:.4f}')
print(f'bound2 (time-forward for retro entry): {fmt(bound2)} JD={bound2:.4f}')

# Sort chronologically
bounds = sorted([b for b in [bound1, bound2] if b is not None])
print(f'After sort:')
print(f'  ENTRY (min JD, past):  {fmt(bounds[0])}')
print(f'  EXIT  (max JD, future): {fmt(bounds[1])}')
print()
print('Expected: Rahu entered Kumbha ~May 18, 2025 | exits ~Dec 5, 2026')

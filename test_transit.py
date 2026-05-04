import swisseph as swe, pytz, datetime

swe.set_sid_mode(swe.SIDM_LAHIRI)
PLANET_FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED
local_tz = pytz.timezone('Asia/Kolkata')
months_en = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
LAGNA_EN = ['Mesha','Vrushabha','Mithuna','Karkadaka','Simha','Kanya','Tula','Vrushchika','Dhanassu','Makara','Kumbha','Meena']

# Current approximate JD (April 16, 2026, 8:30 UTC)
jd_now = swe.julday(2026, 4, 16, 8.5)

def get_lon(jd_val, name, pid):
    if name in ('Ketu', 'Chitra', 'Mitra'):
        r = swe.calc_ut(jd_val, swe.TRUE_NODE, PLANET_FLAGS)[0][0]
        if name == 'Ketu':   return (r + 180) % 360
        if name == 'Chitra': return (r + 3.3333) % 360
        if name == 'Mitra':  return ((r + 180) % 360 + 3.3333) % 360
    if name == 'Bhoomi':
        s = swe.calc_ut(jd_val, swe.SUN, PLANET_FLAGS)[0][0]
        return (s + 180) % 360
    return swe.calc_ut(jd_val, pid, PLANET_FLAGS)[0][0]

def is_retro(jd_val, name, pid):
    ALWAYS_RETRO = {'Ketu', 'Rahu', 'Chitra', 'Mitra'}
    if name in ALWAYS_RETRO: return True
    if pid is None: return False
    return swe.calc_ut(jd_val, pid, PLANET_FLAGS)[0][3] < 0

def find_boundary(jd_start, name, pid, lagna_idx, find_exit):
    # FIXED LOGIC: Entry is past (-1), Exit is future (+1)
    direction = 1 if find_exit else -1
    
    step_map = {'Chandra': 0.5, 'Surya': 3, 'Bhoomi': 3, 'Budha': 2,
                'Sukra': 3, 'Kuja': 5, 'Guru': 15, 'Sani': 30,
                'Rahu': 15, 'Ketu': 15, 'Chitra': 15, 'Mitra': 15}
    step = step_map.get(name, 10)
    jd_a = jd_start
    for _ in range(int(3600/step)+2): # Look up to 10 years for slow planets
        jd_b = jd_a + direction * step
        lon_b = get_lon(jd_b, name, pid)
        if int(lon_b/30)%12 != lagna_idx:
            lo, hi = min(jd_a,jd_b), max(jd_a,jd_b)
            for _ in range(35):
                mid = (lo+hi)/2
                if int(get_lon(mid,name,pid)/30)%12 == lagna_idx:
                    if direction > 0: lo = mid
                    else: hi = mid
                else:
                    if direction > 0: hi = mid
                    else: lo = mid
            return hi if direction > 0 else lo
        jd_a = jd_b
    return None

def fmt(jd_val):
    if jd_val is None: return 'N/A'
    y,m,d,h = swe.revjul(jd_val)
    dt = datetime.datetime(int(y),int(m),int(d)) + datetime.timedelta(hours=h)
    dt = pytz.utc.localize(dt).astimezone(local_tz)
    return f'{dt.day:2d} {months_en[dt.month-1]} {dt.year} {dt.strftime("%H:%M:%S")} IST'

PLANETS_12 = [
    ('Surya',  swe.SUN),   ('Chandra', swe.MOON),   ('Kuja',  swe.MARS),
    ('Budha',  swe.MERCURY),('Guru',   swe.JUPITER), ('Sukra', swe.VENUS),
    ('Sani',   swe.SATURN), ('Rahu',   swe.MEAN_NODE),
    ('Ketu',   None),       ('Bhoomi', None),         ('Chitra', None), ('Mitra', None)
]

print(f"{'Planet':<10} {'Lagnam':<12} {'Retro':<7} {'Entry (IST)':<26} {'Exit (IST)':<26}")
print('-'*83)
for name, pid in PLANETS_12:
    lon = get_lon(jd_now, name, pid)
    lagna_idx = int(lon/30) % 12
    retro = is_retro(jd_now, name, pid)
    entry_jd = find_boundary(jd_now, name, pid, lagna_idx, find_exit=False)
    exit_jd  = find_boundary(jd_now, name, pid, lagna_idx, find_exit=True)
    print(f"{name:<10} {LAGNA_EN[lagna_idx]:<12} {str(retro):<7} {fmt(entry_jd):<28} {fmt(exit_jd):<28}")

import datetime
import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)

TELUGU_YEARS = [
    "ప్రభవ", "విభవ", "శుక్ల", "ప్రమోదూత", "ప్రజోత్పత్తి", "ఆంగీరస", "శ్రీముఖ", "భావ", "యువ", "ధాత",
    "ఈశ్వర", "బహుధాన్య", "ప్రమాది", "విక్రమ", "వృష", "చిత్రభాను", "స్వభాను", "తారణ", "పార్థివ", "వ్యయ",
    "సర్వజిత్తు", "సర్వధారి", "విరోధి", "వికృతి", "ఖర", "నందన", "విజయ", "జయ", "మన్మథ", "దుర్ముఖి",
    "హేవిలంబి", "విలంబి", "వికారి", "శార్వరి", "ప్లవ", "శుభకృతు", "శోభకృతు", "క్రోధి", "విశ్వావసు", "పరాభవ",
    "ప్లవంగ", "కీలక", "సౌమ్య", "సాధారణ", "విరోధికృతు", "పరీధావి", "ప్రమాదీచ", "ఆనంద", "రాక్షస", "నల",
    "పింగళ", "కాళయుక్తి", "సిద్ధార్థి", "రౌద్రి", "దుర్మతి", "దుందుభి", "రుధిరోద్గారి", "రక్తాక్షి", "క్రోధన", "అక్షయ"
]
TELUGU_MASALU = [
    "చైత్ర", "వైశాఖ", "జ్యేష్ఠ", "ఆషాఢ", "శ్రావణ", "భాద్రపద", 
    "ఆశ్వయుజ", "కార్తీక", "మార్గశిర", "పుష్య", "మాఘ", "ఫాల్గుణ"
]

def find_amavasya(jd_guess):
    jd_val = jd_guess
    for _ in range(10):
        m = swe.calc_ut(jd_val, swe.MOON)[0][0]
        s = swe.calc_ut(jd_val, swe.SUN)[0][0]
        df = (m - s) % 360
        if df > 180: df -= 360
        jd_val -= df / 12.190749
        if abs(df) < 0.0001:
            break
    return jd_val

def get_year(dt_str):
    dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    year = dt.year
    month = dt.month

    # get jd
    utc_dt = dt # roughly
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60)

    # masam
    moon_lon = swe.calc_ut(jd, swe.MOON)[0][0]
    sun_lon = swe.calc_ut(jd, swe.SUN)[0][0]
    diff_moon_sun = (moon_lon - sun_lon) % 360
    days_since = diff_moon_sun / 12.190749
    jd_start = find_amavasya(jd - days_since)
    
    amavasya_sun_lon = swe.calc_ut(jd_start, swe.SUN)[0][0]
    rasi_idx = int((amavasya_sun_lon % 360) / 30)
    masam_index = (rasi_idx + 1) % 12
    telugu_masam_name = TELUGU_MASALU[masam_index]

    if month <= 6 and masam_index >= 9:
        adj_year = year - 1
    else:
        adj_year = year

    year_index = (adj_year - 1987) % 60
    return TELUGU_YEARS[year_index], telugu_masam_name, masam_index

print("2026-03-21:", get_year("2026-03-21 12:00"))  # Parabhava, Chaitra
print("2026-03-15:", get_year("2026-03-15 12:00"))  # Vishwavasu, Phalguna
print("2024-04-10:", get_year("2024-04-10 12:00"))  # Krodhi, Chaitra

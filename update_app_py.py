import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\KRISH\.gemini\antigravity\scratch\Timeastro\app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Helper function definition to insert at top
helper_code = '''
def get_timezone_str(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
        if 6.0 <= lat <= 38.0 and 68.0 <= lon <= 98.0:
            return "Asia/Kolkata"
        try:
            from timezonefinder import TimezoneFinder
            tf = TimezoneFinder()
            if hasattr(tf, 'timezone_at'):
                tz = tf.timezone_at(lat=lat, lng=lon) or tf.timezone_at(lng=lon, lat=lat)
            elif hasattr(tf, 'certain_timezone_at'):
                tz = tf.certain_timezone_at(lat=lat, lng=lon)
            else:
                tz = None
            if tz:
                return tz
        except Exception:
            pass
        try:
            import timezonefinderL
            tf = timezonefinderL.TimezoneFinder()
            tz = tf.timezone_at(lng=lon, lat=lat)
            if tz:
                return tz
        except Exception:
            pass
    except Exception as e:
        print("[get_timezone_str error]:", e)
    return "Asia/Kolkata"
'''

if 'def get_timezone_str(' not in code:
    # Insert helper before get_kundali_data
    pos = code.find('def get_kundali_data(')
    if pos != -1:
        code = code[:pos] + helper_code + "\n\n" + code[pos:]

# Replace timezonefinder block inside get_kundali_data
old_tf_block1 = '''    # Determine Timezone based on Latitude and Longitude
    try:
        from timezonefinder import TimezoneFinder
        tf = TimezoneFinder()
        timezone_str = tf.certain_timezone_at(lat=lat, lng=lon)
        if not timezone_str:
            timezone_str = "Asia/Kolkata"
    except ImportError:
        timezone_str = "Asia/Kolkata"'''

new_tf_block1 = '''    # Determine Timezone based on Latitude and Longitude
    timezone_str = get_timezone_str(lat, lon)'''

if old_tf_block1 in code:
    code = code.replace(old_tf_block1, new_tf_block1)

old_tf_block2 = '''    try:
        from timezonefinder import TimezoneFinder
        tf = TimezoneFinder()
        timezone_str = tf.certain_timezone_at(lat=lat, lng=lon) or "Asia/Kolkata"
    except ImportError:
        timezone_str = "Asia/Kolkata"'''

if old_tf_block2 in code:
    code = code.replace(old_tf_block2, new_tf_block1)

with open(r'C:\Users\KRISH\.gemini\antigravity\scratch\Timeastro\app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Successfully updated app.py with crash-proof get_timezone_str!")

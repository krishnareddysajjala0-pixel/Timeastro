import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\KRISH\.gemini\antigravity\scratch\Timeastro\templates\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

auto_init_script = '''
        // Auto-fill mobile date, time, and location permission request on app launch
        document.addEventListener('DOMContentLoaded', function() {
            var dobElem = document.getElementById('dob');
            var tobElem = document.getElementById('tob');
            var now = new Date();

            if (dobElem && !dobElem.value) {
                var yyyy = now.getFullYear();
                var mm = String(now.getMonth() + 1).padStart(2, '0');
                var dd = String(now.getDate()).padStart(2, '0');
                dobElem.value = yyyy + '-' + mm + '-' + dd;
            }

            if (tobElem && !tobElem.value) {
                var hh = String(now.getHours()).padStart(2, '0');
                var min = String(now.getMinutes()).padStart(2, '0');
                tobElem.value = hh + ':' + min;
            }

            // Auto-request location permission & location lookup if lat/lon not set
            var latElem = document.getElementById('lat');
            var lonElem = document.getElementById('lon');
            if (latElem && lonElem && (!latElem.value || !lonElem.value)) {
                setTimeout(function() {
                    if (typeof getCurrentLocation === 'function') {
                        getCurrentLocation();
                    }
                }, 500);
            }
        });
'''

target = "// Hide loader on back/forward cache"
if target in html and 'Auto-fill mobile date, time, and location' not in html:
    html = html.replace(target, auto_init_script + "\n        " + target)

with open(r'C:\Users\KRISH\.gemini\antigravity\scratch\Timeastro\templates\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully updated templates/index.html with default date, time, and auto-location request!")

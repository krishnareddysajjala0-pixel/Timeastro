import os
import sys
import threading
import urllib.request

_state_lock = threading.Lock()
_server_running = False


def _is_health_up():
    try:
        with urllib.request.urlopen("http://127.0.0.1:5000/health", timeout=0.5) as resp:
            return resp.status == 200
    except Exception:
        return False


def start_server():
    global _server_running
    if _is_health_up():
        print("[Ravan Astro Server] Server already responding on 127.0.0.1:5000")
        return

    with _state_lock:
        if _server_running:
            print("[Ravan Astro Server] Server start already in progress")
            return
        _server_running = True

    try:
        # Set current working directory to python bundle dir so relative paths resolve correctly
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(bundle_dir)
        if bundle_dir not in sys.path:
            sys.path.insert(0, bundle_dir)

        # Alias timezonefinder to timezonefinderL (pure Python lightweight version)
        try:
            import timezonefinderL as tf_light
            if hasattr(tf_light, 'TimezoneFinderL') and not hasattr(tf_light, 'TimezoneFinder'):
                setattr(tf_light, 'TimezoneFinder', tf_light.TimezoneFinderL)
            sys.modules['timezonefinder'] = tf_light
        except Exception as e:
            print("[Ravan Astro Launcher] timezonefinderL alias notice:", e)

        print(f"[Ravan Astro Server] Starting embedded Flask server from {bundle_dir}...")

        # Import app module dynamically after setting up paths and aliases
        from app import app

        # Run Flask server locally on port 5000
        app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False, threaded=True)
    except OSError as e:
        print("[Ravan Astro Server] Socket/startup notice:", e)
    finally:
        with _state_lock:
            _server_running = False

if __name__ == "__main__":
    start_server()

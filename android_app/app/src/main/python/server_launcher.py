import os
import sys

def start_server():
    # Set current working directory to python bundle dir so relative paths resolve correctly
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(bundle_dir)
    if bundle_dir not in sys.path:
        sys.path.insert(0, bundle_dir)

    # Alias timezonefinder to timezonefinderL (pure Python lightweight version)
    try:
        import timezonefinderL as tf_light
        sys.modules['timezonefinder'] = tf_light
    except Exception as e:
        print("[Timeastro Launcher] timezonefinderL alias notice:", e)

    print(f"[Timeastro Server] Starting embedded Flask server from {bundle_dir}...")
    
    # Import app module dynamically after setting up paths and aliases
    from app import app
    
    # Run Flask server locally on port 5000
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    start_server()

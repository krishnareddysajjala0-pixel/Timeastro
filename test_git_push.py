import subprocess
import datetime

try:
    with open("user_data.txt", "a", encoding="utf-8") as f:
        f.write(f"\nTest Log: {datetime.datetime.now()}")

    subprocess.run(["git", "add", "user_data.txt"], check=True, capture_output=True, text=True)
    res_commit = subprocess.run(["git", "commit", "-m", "Log new user data test"], check=True, capture_output=True, text=True)
    print("Commit output:", res_commit.stdout)
    res_push = subprocess.run(["git", "push"], check=True, capture_output=True, text=True)
    print("Push output:", res_push.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    print(f"Stdout: {e.stdout}")
    print(f"Stderr: {e.stderr}")

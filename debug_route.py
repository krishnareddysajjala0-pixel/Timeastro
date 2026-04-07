import sys
import traceback

try:
    from app import app
    with app.test_client() as c:
        response = c.get('/daily_panchangam')
        print(f'Status: {response.status_code}')
        if response.status_code != 200:
            print(response.data.decode('utf-8'))
except Exception:
    traceback.print_exc()

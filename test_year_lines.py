from app import app
import traceback

with app.test_request_context():
    try:
        with app.test_client() as client:
            resp = client.post('/chart', data={
                'name': 'Test User',
                'dob': '2026-03-21',
                'tob': '12:00',
                'place': 'Hyderabad',
                'lat': '17.3850',
                'lon': '78.4867'
            })
            html = resp.data.decode('utf-8')
            for line in html.split('\n'):
                if 'సంవత్సరం' in line:
                    print("YEAR LINE:", line.strip())
            
            resp3 = client.post('/chart', data={
                'name': 'Test User',
                'dob': '2026-03-15',
                'tob': '12:00',
                'place': 'Hyderabad',
                'lat': '17.3850',
                'lon': '78.4867'
            })
            html3 = resp3.data.decode('utf-8')
            for line in html3.split('\n'):
                if 'సంవత్సరం' in line:
                    print("YEAR LINE (Mar 15):", line.strip())
                    
    except Exception as e:
        traceback.print_exc()

import requests
import datetime
import threading
from app import app

def test_chart():
    with app.test_client() as client:
        # March 21, 2026 should be Parabhava since the Telugu month is Chaitra
        response = client.post('/chart', data={
            'name': 'Test User',
            'dob': '2026-03-21',
            'tob': '12:00',
            'place': 'Hyderabad',
            'lat': '17.3850',
            'lon': '78.4867'
        })
        
        # Also check April 10, 2024 to verify it's Krodhi
        response2 = client.post('/chart', data={
            'name': 'Test User',
            'dob': '2024-04-10',
            'tob': '12:00',
            'place': 'Hyderabad',
            'lat': '17.3850',
            'lon': '78.4867'
        })
        
        # March 15, 2026 should be Vishwavasu since it's before Chaitra
        response3 = client.post('/chart', data={
            'name': 'Test User',
            'dob': '2026-03-15',
            'tob': '12:00',
            'place': 'Hyderabad',
            'lat': '17.3850',
            'lon': '78.4867'
        })

if __name__ == '__main__':
    from flask import session
    with app.test_request_context():
        # Let's just mock the chart function logic directly or use the test client
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
            if 'పరాభవ' in html:
                print("2026-03-21 is Parabhava! SUCCESS")
            else:
                print("2026-03-21 FAILED")
                print([line for line in html.split('\\n') if 'సంవత్సరం' in line])
                
            resp2 = client.post('/chart', data={
                'name': 'Test User',
                'dob': '2024-04-10',
                'tob': '12:00',
                'place': 'Hyderabad',
                'lat': '17.3850',
                'lon': '78.4867'
            })
            html2 = resp2.data.decode('utf-8')
            if 'క్రోధి' in html2:
                print("2024-04-10 is Krodhi! SUCCESS")
            else:
                print("2024-04-10 FAILED")
                
            resp3 = client.post('/chart', data={
                'name': 'Test User',
                'dob': '2026-03-15',
                'tob': '12:00',
                'place': 'Hyderabad',
                'lat': '17.3850',
                'lon': '78.4867'
            })
            html3 = resp3.data.decode('utf-8')
            if 'విశ్వావసు' in html3:
                print("2026-03-15 is Vishwavasu! SUCCESS")
            else:
                print("2026-03-15 FAILED")


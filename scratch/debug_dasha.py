
import sys
import os
from flask import Flask, session
import datetime
import pytz

# Add the project directory to sys.path
sys.path.append(r'C:\Users\gnana\.gemini\antigravity\scratch\Timeastro')

from app import app, get_kundali_data, get_dasha_info

def test_compare_dasha():
    with app.test_request_context():
        # Mock data (you might need to adjust based on real data)
        name1 = "Test1"
        dob1 = "1990-01-01"
        tob1 = "12:00"
        place1 = "Hyderabad, India"
        lat1 = 17.3850
        lon1 = 78.4867

        name2 = "Test2"
        dob2 = "1992-05-05"
        tob2 = "15:30"
        place2 = "Bangalore, India"
        lat2 = 12.9716
        lon2 = 77.5946

        print("Testing get_kundali_data 1...")
        data1 = get_kundali_data(name1, dob1, tob1, place1, lat1, lon1)
        print("Testing get_kundali_data 2...")
        data2 = get_kundali_data(name2, dob2, tob2, place2, lat2, lon2)

        print("Testing get_dasha_info 1...")
        dasha1 = get_dasha_info(data1)
        print("Testing get_dasha_info 2...")
        dasha2 = get_dasha_info(data2)

        print("Success in logic!")

if __name__ == "__main__":
    try:
        test_compare_dasha()
    except Exception as e:
        import traceback
        traceback.print_exc()

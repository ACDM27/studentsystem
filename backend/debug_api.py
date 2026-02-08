import requests
import sys

try:
    print("Testing API connection...")
    r = requests.get('http://localhost:8000/api/v1/common/teachers')
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Error: {e}")

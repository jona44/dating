import requests
import json

url = "http://127.0.0.1:8000/api/auth/token/"
headers = {"Content-Type": "application/json"}

# Test 1: Correct email and password
payload1 = {"email": "testuser700@gmail.com", "password": "Password123!"}
print(f"Testing Payload: {payload1}")
try:
    response = requests.post(url, json=payload1)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

print("-" * 20)

# Test 2: Username instead of email (simulating app issue)
payload2 = {"username": "testuser700@gmail.com", "password": "Password123!"}
print(f"Testing Payload: {payload2}")
try:
    response = requests.post(url, json=payload2)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

import requests
import json

url = "http://127.0.0.1:8000/api/auth/token/"
data = {
    "username": "testuser700@gmail.com",
    "password": "Password123!"
}
response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")

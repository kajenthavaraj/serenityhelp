# send_request.py
import requests

url = "http://localhost:8000/analyze"
text_to_analyze = "I hear voices and I feel like I'm not myself."

response = requests.post(url, json={"text": text_to_analyze})

print("Status Code:", response.status_code)
print("Response:", response.json())

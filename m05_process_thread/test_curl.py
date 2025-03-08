import requests

url = "http://localhost:8000/execute"
data = {"code": "print('Hello')", "timeout": 5}

response = requests.post(url, data=data)
print(response.status_code, response.json())
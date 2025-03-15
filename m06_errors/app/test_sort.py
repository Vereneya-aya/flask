import requests

url = "http://127.0.0.1:5000/tim/"
data = {"numbers": [10, 3, 8, 2]}
response = requests.post(url, json=data)
print(response.json())
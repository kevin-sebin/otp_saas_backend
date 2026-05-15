import requests

API_KEY = "ob2qXDyVZBIs_-_tdk3f21yyMNa9dzXZ7GTfHlgPyMo"

url = "http://127.0.0.1:8000/send-otp"
payload = {"email": "kevinsebinkk@gmail.com"}
headers = {"x-api-key": API_KEY}
response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(response.text)

url = "http://127.0.0.1:8000/verify"
headers = {"x-api-key": "ob2qXDyVZBIs_-_tdk3f21yyMNa9dzXZ7GTfHlgPyMo"}
data = {"email": "kevinsebinkk@gmail.com", "otp": str(input())}
response = requests.post(url, json=data,headers=headers)
print(response.status_code)
print(response.text)
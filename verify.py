import requests

API_KEY = "API_KEY"
registered_email = 'EMAIL'

url = "http://127.0.0.1:8000/send-otp"
payload = {"email": registered_email}
headers = {"x-api-key": API_KEY}
response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(response.text)

url = "http://127.0.0.1:8000/verify"
headers = {"x-api-key": API_KEY}
data = {"email": registered_email, "otp": str(input())}
response = requests.post(url, json=data,headers=headers)
print(response.status_code)
print(response.text)
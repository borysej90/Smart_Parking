import requests

BASE = 'http://127.0.0.1:5000/'

response = requests.get(BASE + 'parking/ Yeet Prospect/all')
print(response.json())

#response = requests.post(BASE + 'parking/Yeet Prospect/lot_number/2/is_paid/1')
#print(response.json())
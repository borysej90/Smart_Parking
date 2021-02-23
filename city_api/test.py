import requests

BASE = 'http://127.0.0.1:5000/'

response = requests.get(BASE + 'parking/Prospect P')
print(response.json())

response = requests.get(BASE + 'parking/Prospect Ratushnyaka/lot_number/2')
print(response.json())



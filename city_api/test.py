import requests

BASE = 'http://127.0.0.1:5000/'

# response = requests.get(BASE + 'parking/Yeet_Prospect/lot_number/1')
# print(response.json())

response = requests.post('http://127.0.0.1:5000/parking/Yeet_Prospect/lot_number/4/is_paid/1')
print(response.json())
#response = requests.post(BASE + 'parking/Yeet_Prospect/lot_number/2/is_paid/1')
#print(response.json())

#response = requests.post(BASE + 'parking/Yeet_Prospect/lot_number/2/is_paid/1')
#print(response.json())
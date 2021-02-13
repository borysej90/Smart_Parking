import requests

BASE = 'http://127.0.0.1:5000/'

data = [{"is_paid": True, "parking_slot": 1},
        {"is_paid": True, "parking_slot": 2},
        {"is_paid": False, "parking_slot": 3},
        ]
# Put some data
#for i in range(len(data)):
#   response = requests.put(BASE + "parking/" + str(i) , data[i])
#   print(response.json())

# GET all parking info
#for i in range(0,3):
#     response = requests.get(BASE + 'parking/' + str(i))
#     print(response.json())

# GET info about specific parking slot
# parking_id = i -> slot_id = i+1 ON THIS VERSION ONLY I HOPE
#response = requests.get(BASE + 'parking/1/slot/2')
#print(response.json())
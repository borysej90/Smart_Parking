import requests

BASE = 'http://127.0.0.1:5000/'

data = [{"total_lots":100,"free_lots":23},
        {"total_lots":75,"free_lots":45},
        {"total_lots":50,"free_lots":29},
        ]
# Put some data
for i in range(len(data)):
    response = requests.put(BASE + "parking/" + str(i), data[i])
    print(response.json())

# GET parking space with id - 1
response = requests.get(BASE + "parking/1")
print(response.json())


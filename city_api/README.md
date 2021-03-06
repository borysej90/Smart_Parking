## City API Endpoints Usage

###Initial steps

First you have to run `main.py`.It will connect to Database `database.db`, 
after that you can use Endpoints.

###POST
There are few types of `POST` 

####1._Posts parking site_
```angular2html
response = requests.post('http://127.0.0.1:5000/parking/Yeet_Street')
print(response.json())
```
**Returns `200` if everything is ok**
 

Response Example:

`{'id': 2, 'address': 'Yeet_Street'}`

####2._Posts parking lot_ 
```angular2html
response = requests.post('http://127.0.0.1:5000/parking/Yeet_Prospect/lot_number/4/is_paid/1')
print(response.json())
```

####_NOTE: You have to create parking site before assigning any lots to it_

Response Exmaple:

`{'site_id': 1, 'lot_id': 4, 'is_paid': True, 'lot_number': 4, 'address': 'Yeet_Prospect'}`
###GET

There are differenct types of `GET` endpoint

####1.Gets all info about parking site

```angular2html
response = requests.get('http://127.0.0.1:5000/parking/Yeet_Prospect/all')
print(response.json())
```


Response Example:
```angular2html
[{'site_id': 1, 'lot_id': 1, 'is_paid': True, 'lot_number': 1, 'address': 'Yeet_Prospect'},
 {'site_id': 1, 'lot_id': 2, 'is_paid': True, 'lot_number': 2, 'address': 'Yeet_Prospect'},
 {'site_id': 1, 'lot_id': 3, 'is_paid': False, 'lot_number': 3, 'address': 'Yeet_Prospect'}
]
```

####2.Gets info about specified parking lot

```angular2html
response = requests.get('http://127.0.0.1:5000/parking/Yeet_Prospect/lot_number/1')
print(response.json())
```

Response Example: 
```angular2html
{'site_id': 1, 'lot_id': 1, 'is_paid': True, 'lot_number': 1, 'address': 'Yeet_Prospect'}
```

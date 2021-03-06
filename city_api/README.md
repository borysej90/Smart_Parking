## City API Endpoints Usage

### Initial steps

First you have to run `main.py`.It will connect to Database `database.db`, 
after that you can use Endpoints.

### POST
There are few types of `POST` 

#### 1._Parking site_
```http 
POST /parking/<string:address>
```

#### Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `parking` | `string` | **Required**. Address of parking site |


Response Example:

```json
{"id": 2, "address": "Yeet_Street"}
```


| Key | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Id of the specified parking site. |
| `address` | `string` | Address of the specified parking site. |

| Status Code | Condition |
| :--- | :--- |
| 400 `BAD REQUEST` | The parking site already exists. |

#### 2._Parking lot_ 
```http
POST /parking/<string:address>/lot_number/<int:lot_number>/is_paid/<int:is_paid>
```

#### Parameters
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `parking` | `string` | **Required**. Address of parking site |
| `lot_number` | `int` | **Required**. Number of parking lot |
| `is_paid` | `int` | **Required**. Was parking paid for |


Response Exmaple:

```json
{"site_id": 1, "lot_id": 4, "is_paid": true, "lot_number": 4, "address": "Yeet_Prospect"}
```

| Key | Type | Description |
| :--- | :--- | :--- |
| `site_id` | `int` | Id of the specified parking site. |
| `lot_id` | `int` | Id of the specified parking lot. |
| `lot_number` | `int` |  Number of specified parking lot |
| `is_paid` | `bool` |  Was parking paid for |
| `address` | `string` | Address of the specified parking site. |


| Status Code | Condition |
| :--- | :--- |
| 400 `BAD REQUEST` | The parking lot already exists. |
| 404 `NOT FOUND` | The parking site does not exist. |

### GET

#### 1.GET all info about parking site

```http
GET /parking/<string:address>/all
```

#### Parameters
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `parking` | `string` | **Required**. Address of parking site |


Response Example:

_NOTE:_ response type is `Array`
```json
[
  {"site_id": 1, "lot_id": 1, "is_paid": true, "lot_number": 1, "address": "Yeet_Prospect"},
  {"site_id": 1, "lot_id": 2, "is_paid": true, "lot_number": 2, "address": "Yeet_Prospect"},
  {"site_id": 1, "lot_id": 3, "is_paid": false, "lot_number": 3, "address": "Yeet_Prospect"}
]
```
| Key | Type | Description |
| :--- | :--- | :--- |
| `site_id` | `int` | Id of the specified parking site. |
| `lot_id` | `int` | Id of the specified parking lot. |
| `lot_number` | `int` |  Number of specified parking lot |
| `is_paid` | `bool` | Was parking paid for |
| `address` | `string` | Address of the specified parking site. |

| Status Code | Condition |
| :--- | :--- |
| 404 `NOT FOUND` | The parking site does not exist. |
| 404 `NOT FOUND` | The parking site does not have any lots. |

#### 2.GET info about specified parking lot

```http
GET /parking/<string:address>/lot_number/<int:lot_number>
```

#### пParameters
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `parking` | `string` | **Required**. Address of parking site |
| `lot_number` | `string` | **Required**. Number of parking lot |

Response Example: 
```json
{"site_id": 1, "lot_id": 1, "is_paid": true, "lot_number": 1, "address": "gYeet_Prospect"}
```
| Key | Type | Description |
| :--- | :--- | :--- |
| `site_id` | `int` | Id of the specified parking site. |
| `lot_id` | `int` | Id of the specified parking lot. |
| `lot_number` | `int` |  Number of specified parking lot |
| `is_paid` | `bool` | Was parking paid for |
| `address` | `string` | Address of the specified parking site. |

| Status Code | Condition |
| :--- | :--- |
| 404 `NOT FOUND` | The parking site or lot does not exist. |

## Use PostgreSQL in docker

#### Initial steps

Firstly, you have to install **Docker** on your system.

Then, you can run command below:

```bash
sudo docker run -d --rm --name smart_parking_db -p 5555:5432 -e POSTGRES_USER=smart_parking_user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=smart_parking postgres:13
```

*NOTE: if you are running Windows then run commands without `sudo`*

The command above will set up clean PostgreSQL with no data in it each time you run it - good for testing.

#### Add persistence to database

If you want to save data between your DB reloads then firtsly create new Docker volume:

```bash
sudo docker volume create smart_parking_volume
```

After this run updated version of `docker run` command:

```bash
sudo docker run -d --rm --name smart_parking_db -v smart_parking_volume:/var/lib/postgresql/data -p 5555:5432 -e POSTGRES_USER=smart_parking_user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=smart_parking postgres:13
```

#### Stop database

To stop Docker container just type this:

```bash
sudo docker stop smart_parking_db
```

#### Update Django with new DB

Create `.env` file in this directory if you haven't done it before. Then add these lines to it:

```
DB_NAME=smart_parking
DB_USER=smart_parking_user
DB_PASSWORD=password
DB_PORT=5555
```

## API Documentation

## Parking lots

#### Request

```http
GET /api/sites/<int:site_id>/lots/
```

#### Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `site_id` | `int` | **Required**. ID of parking site |

#### Responses

*NOTE: response type is `Array`*

```json
[
  {
    "id": 1,
    "parking_site_id": 1,
    "coordinates": [
      65, 121,
      82, 119,
      62, 135,
      93, 130
    ],
    "is_occupied": true,
    "is_for_disabled": true
  },
  {
    "id": 5,
    "parking_site_id": 1,
    "coordinates": [
      87, 256,
      120, 259,
      82, 290,
      125, 289
    ],
    "is_occupied": true,
    "is_for_disabled": false
  }
]
```

| Key | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Id of the current parking lot. |
| `parking_site_id` | `int` | Id of the current parking site. |
| `coordinates` | `array<int>` | Visual coordinates of the current parking lot. <br /> *Format: [x1, y1, x2, y2, x3, y3, x4, y4]*|
| `is_occupied` | `boolean` | Describes if the parking lot is occupied. |
| `is_for_disabled` | `boolean` | Describes if the parking lot is for people with disabilities. |

#### Status Codes

| Status Code | Condition |
| :--- | :--- |
| 404 `NOT FOUND` | The parking site was not found. |

---

#### Request

```http
POST /api/sites/<int:site_id>/lots/
```

#### Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `site_id` | `int` | **Required**. ID of parking site |

#### Body

*NOTE: request type is `Array`*

```json
[
  {
    "parking_site_id": 1,
    "coordinates": [
      65, 121,
      82, 119,
      62, 135,
      93, 130
    ],
    "is_occupied": true,
    "is_for_disabled": true
  },
  {
    "parking_site_id": 1,
    "coordinates": [
      87, 256,
      120, 259,
      82, 290,
      125, 289
    ],
    "is_occupied": true,
    "is_for_disabled": false
  }
]
```

| Key | Type | Description |
| :--- | :--- | :--- |
| `parking_site_id` | `int` | Id of the current parking site. |
| `coordinates` | `array<int>` | Visual coordinates of the current parking lot. <br /> *Format: [x1, y1, x2, y2, x3, y3, x4, y4]* |
| `is_occupied` | `boolean` | Describes if the parking lot is occupied. |
| `is_for_disabled` | `boolean` | Describes if the parking lot is for people with disabilities. |

#### Responses

*NOTE: response type is `Array`*

```json
[
  {
    "id": 1,
    "parking_site_id": 1,
    "coordinates": [
      65, 121,
      82, 119,
      62, 135,
      93, 130
    ],
    "is_occupied": true,
    "is_for_disabled": true
  },
  {
    "id": 5,
    "parking_site_id": 1,
    "coordinates": [
      87, 256,
      120, 259,
      82, 290,
      125, 289
    ],
    "is_occupied": true,
    "is_for_disabled": false
  }
]
```

| Key | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Id of the current parking lot. |
| `parking_site_id` | `int` | Id of the current parking site. |
| `coordinates` | `array<int>` | Visual coordinates of the current parking lot. <br /> *Format: [x1, y1, x2, y2, x3, y3, x4, y4]* |
| `is_occupied` | `boolean` | Describes if the parking lot is occupied. |
| `is_for_disabled` | `boolean` | Describes if the parking lot is for people with disabilities. |

#### Status Codes

| Status Code | Condition |
| :--- | :--- |
| 400 `NOT FOUND` | Request body is invalid. |

---

#### Request

```http
GET /api/sites/<int:site_id>/lots/<int:id>/
```

#### Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `site_id` | `int` | **Required**. ID of parking site |
| `id` | `int` | **Required**. ID of parking lot |

#### Responses

```json
{
  "id": 1,
  "parking_site_id": 1,
  "coordinates": [
    65, 121,
    82, 119,
    62, 135,
    93, 130
  ],
  "is_occupied": true,
  "is_for_disabled": true
}
```

| Key | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Id of the current parking lot. |
| `parking_site_id` | `int` | Id of the current parking site. |
| `coordinates` | `array<int>` | Visual coordinates of the current parking lot. <br /> *Format: [x1, y1, x2, y2, x3, y3, x4, y4]* |
| `is_occupied` | `boolean` | Describes if the parking lot is occupied. |
| `is_for_disabled` | `boolean` | Describes if the parking lot is for people with disabilities. |

#### Status Codes

| Status Code | Condition |
| :--- | :--- |
| 400 `BAD REQUEST` | The parking site does not contain the requested parking lot. |
| 404 `NOT FOUND` | The parking site was not found. |

---

#### Request

```http
PUT /api/sites/<int:site_id>/lots/<int:id>/
```

#### Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `site_id` | `int` | **Required**. ID of parking site |
| `id` | `int` | **Required**. ID of parking lot |

#### Body

```json
{
  "id": 1,
  "parking_site_id": 1,
  "coordinates": [
    65, 121,
    82, 119,
    62, 135,
    93, 130
  ],
  "is_occupied": false,
  "is_for_disabled": false
}
```

| Key | Type | Description |
| :--- | :--- | :--- |
| `parking_site_id` | `int` | Id of the current parking site. |
| `coordinates` | `array<int>` | Visual coordinates of the current parking lot. <br /> *Format: [x1, y1, x2, y2, x3, y3, x4, y4]* |
| `is_occupied` | `boolean` | Describes if the parking lot is occupied. |
| `is_for_disabled` | `boolean` | Describes if the parking lot is for people with disabilities. |

#### Responses

```json
{
  "id": 1,
  "parking_site_id": 1,
  "coordinates": [
    65, 121,
    82, 119,
    62, 135,
    93, 130
  ],
  "is_occupied": false,
  "is_for_disabled": false
}
```

| Key | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Id of the current parking lot. |
| `parking_site_id` | `int` | Id of the current parking site. |
| `coordinates` | `array<int>` | Visual coordinates of the current parking lot. <br /> *Format: [x1, y1, x2, y2, x3, y3, x4, y4]* |
| `is_occupied` | `boolean` | Describes if the parking lot is occupied. |
| `is_for_disabled` | `boolean` | Describes if the parking lot is for people with disabilities. |

#### Status Codes

| Status Code | Condition |
| :--- | :--- |
| 400 `BAD REQUEST` | The parking site does not contain the requested parking lot OR request body is invalid. |
| 404 `NOT FOUND` | The parking site was not found. |

---

#### Request

```http
PATCH /api/sites/<int:site_id>/lots/<int:id>/
```

#### Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `site_id` | `int` | **Required**. ID of parking site |
| `id` | `int` | **Required**. ID of parking lot |

#### Body

```json
{
  "is_occupied": true
}
```

| Key | Type | Description |
| :--- | :--- | :--- |
| `parking_site_id` | `int` | Id of the current parking site. |
| `coordinates` | `array<int>` | Visual coordinates of the current parking lot. <br /> *Format: [x1, y1, x2, y2, x3, y3, x4, y4]* |
| `is_occupied` | `boolean` | Describes if the parking lot is occupied. |
| `is_for_disabled` | `boolean` | Describes if the parking lot is for people with disabilities. |

#### Responses

```json
{
  "id": 1,
  "parking_site_id": 1,
  "coordinates": [
    65, 121,
    82, 119,
    62, 135,
    93, 130
  ],
  "is_occupied": true,
  "is_for_disabled": false
}
```

| Key | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | Id of the current parking lot. |
| `parking_site_id` | `int` | Id of the current parking site. |
| `coordinates` | `array<int>` | Visual coordinates of the current parking lot. <br /> *Format: [x1, y1, x2, y2, x3, y3, x4, y4]* |
| `is_occupied` | `boolean` | Describes if the parking lot is occupied. |
| `is_for_disabled` | `boolean` | Describes if the parking lot is for people with disabilities. |

#### Status Codes

| Status Code | Condition |
| :--- | :--- |
| 400 `BAD REQUEST` | The parking site does not contain the requested parking lot OR request body is invalid. |
| 404 `NOT FOUND` | The parking site was not found. |

---

#### Request

```http
DELETE /api/sites/<int:site_id>/lots/<int:id>/
```

#### Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `site_id` | `int` | **Required**. ID of parking site |
| `id` | `int` | **Required**. ID of parking lot |

#### Responses

```
"Parking lot has been deleted!"
```

#### Status Codes

| Status Code | Condition |
| :--- | :--- |
| 400 `BAD REQUEST` | The parking site does not contain the requested parking lot. |
| 404 `NOT FOUND` | The parking site was not found. |

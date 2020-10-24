# json_mock

# Description
json_mock is a mock server to mock json objects. each object is associated with an entity type


# Definitions

## Entity Type

json_mock servers support of multiple type of entities. An entity_type is a list of entities which
are similar by their type

#### example
```
{
  "posts": [{
      "id": 0,
      "reviews": 32,
      "title": "title1",
      "author": "CIQ",
      "views": 100
    },
    {
      "id": 1,
      "reviews": 3,
      "title": "title2",
      "author": "CommerceIQ",
      "views": 10
    }],
  "authors": [{
      "id": 0
      "first_name": "Commerce",
      "last_name": "IQ",
      "posts": 45,
    }]
}
```

## Entity
An entity is an object that holds some information. every entity has a id field. The id field servers as a primary key
for a particular entity_type.


# store.json
Entities are stored in and store.json file. which initially is and empty json object. with every new object
added/modified/deleted, the store.json file gets updated.

### APIs
all APIs are provided below (change host address with correct endpoint).
#### get all entities
Get all entities for an entity_type

```curl --location --request GET '{{HOST_ADDR}}/entities/posts'```

### Get all entities with filters
Filters can also be applied while querying for entities of a particular type. 

```curl --location --request GET '{{HOST_ADDR}}/entities/posts?title=title1&author=CIQ'```

### Get all entities in sorted order
Entities can be retrieved in sorted order as well. supported order `['asc', 'desc']`, default is ascending order
(can be used with filters as well)

```curl --location --request GET '{{HOST_ADDR}}/entities/posts?_sort=views&_order=asc'``` 

### Get entity by id
An entity can be requested by its id as well, (returns 404 if entity not found)

```curl --location --request GET '{{HOST_ADDR}}/entities/posts/0'```

### Add an entity
An entity can be added using the following api(id is mandatory in body and should be same as in request url).

```
curl --location --request PUT '{{HOST_ADDR}}/entities/posts/0' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": 0,
    "reviews": 32,
    "views": 100,
    "author": "CIQ",
    "title": "title1"
}'
```

### Update an entity
Entities can be updated using the following api. 
```
curl --location --request PATCH '{{HOST_ADDR}}/entities/posts/0' \
--header 'Content-Type: application/json' \
--data-raw '{
    "id": 0,
    "reviews": 32,
    "views": 100,
    "author": "CIQ",
    "title": "title1"
}'
```

### Delete an entity
To delete an entity use the following curl.

```curl --location --request DELETE '{{HOST_ADDR}}/entities/posts/0'```

### Reset an entity type
To reset an entity type or with new entities use the following curl.
```
curl --location --request GET '{{HOST_ADDR}}/entities/posts' \
--header 'Content-Type: application/json' \
--data-raw '[
    {
        "reviews": 32,
        "title": "title1",
        "author": "CIQ",
        "id": 0,
        "views": 100
    },
    {
        "reviews": 3,
        "title": "title2",
        "author": "CommerceIQ",
        "id": 1,
        "views": 10
    }
]'
```

### Get All objects
To Get all objects stored use the following curl.

```curl --location --request GET '{{HOST_ADDR}}/entities/'```

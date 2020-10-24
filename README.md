# json_mock

###APIS:

1. GET /<entity_type>/ -> [entities]
2. GET /<entity_type>/Id -> entity
3. GET /<entity_type>?[<param_name>=value]
4. GET /<entity_type>?_sort=<key>&_order=asc/desc
5. POST /<entity_type>
[<entity1>, <entity2>...]

6. PUT /<entity_type>/Id
{
    <key1>: <value1>,
    <key2>: <value2>,
    ...
}


7. PATCH  /<entity_type>/id
{
    <key1>: <value1>,
    <key2>: <value2>,
    ...
}


8. DELETE <entity_type>/id


# racks_routes.py

-----------------------------
```language=python
def get_all_racks()
```
- REST Type: 'get'
- Authentication Required: no
- Roled required: none
- Arguments: none
- Returns:
```language=json
{
    "message": "success"||"ERROR_MESSAGE",
    "racks":[
        {
            "username": "USERNAME",
        },
        {
            "username": "USERNAME",
        },
        {
            "username": "USERNAME",
        },
        TODO: FINISH THIS
    ]
}
```
-----------------------------
```language=python
def create_racks():
```
- REST Type: 'post'
- Authentication Required: yes
- Roled required: none
- Arguments:
```language=json
{
    "start_letter":"START_LETTER",
    "stop_letter":"STOP_LETTER",
    "start_number":"START_NUMBER"||START_NUMBER,
    "stop_number":"STOP_NUMBER"||STOP_NUMBER
}
```
- Returns:
```language=json
{
    "message": "success"||"ERROR_MESSAGE"
}
```
-----------------------------
```language=python
def get_rack_details():
```
- REST Type: 'post'
- Authentication Required: yes
- Roled required: none
- Arguments:
```language=json
{
    "start_letter":"START_LETTER",
    "stop_letter":"STOP_LETTER",
    "start_number":"START_NUMBER"||START_NUMBER,
    "stop_number":"STOP_NUMBER"||STOP_NUMBER
}
```
- Returns:
```language=json
{
    "message": "success"||"ERROR_MESSAGE"
    "racks":[
        {
            TODO: FINISH THIS
        },
    ]
}
```
-----------------------------
```language=python
def delete_racks():
```
- REST Type: 'post'
- Authentication Required: yes
- Roled required: admin
- Arguments:
```language=json
{
    "start_letter":"START_LETTER",
    "stop_letter":"STOP_LETTER",
    "start_number":"START_NUMBER"||START_NUMBER,
    "stop_number":"STOP_NUMBER"||STOP_NUMBER
}
```
- Returns:
```language=json
{
    "message": "success"||"ERROR_MESSAGE"
}
```
-----------------------------

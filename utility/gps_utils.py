import requests

ID = 1
URL = f"http://192.168.43.5:8080/api/fridges/"

def send_GPS_data_to_server(GPS_data):
    # if the fridge with ID = 1 does not exist, the server will create it
    # else only the gps data will be updated
    print("Sending GPS data to server")
    print(GPS_data)

    data = {
        "fridge_id": ID,
        "longitude": GPS_data["longitude"],
        "latitude": GPS_data["latitude"]
    }

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': '6S1eiOl9Kvu3MIIezl9EDYznqvILwaCRU9hNYkBVtu8Z0sH6NMTBkHp3ZAfrnqdS',
        'Authorization': 'Token 62aa1bd2271eedd587232a3259f262fa5b578d88'
    }

    response = requests.post(URL, json=data, headers=headers)
    print(response.status_code)

    # status code 201 means a new fridge was created, 200 means the fridge already exists and I only updated the gps data 

    if response.status_code not in (200, 201):
        raise AssertionError("GPS data could not be sent")

    print("GPS data sent to server")
    print(response.status_code)
    return response.status_code

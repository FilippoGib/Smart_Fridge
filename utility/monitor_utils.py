
import requests
from datetime import datetime
from src.camera_hanlder import CameraHandler


ID = 1
URL = f"http://192.168.43.5:8080/api/fridges/{ID}/products"


def send_product_to_server(barcode, date, name, ID, URL): #json format
    data = {
         "fridge": ID,
         "barcode": f"{barcode}",
         "expire_date": f"{date}",
         "name": f"{name}"
    }
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': '6S1eiOl9Kvu3MIIezl9EDYznqvILwaCRU9hNYkBVtu8Z0sH6NMTBkHp3ZAfrnqdS',
        'Authorization': 'Token 62aa1bd2271eedd587232a3259f262fa5b578d88'
    }

    response = requests.post(URL, json=data, headers=headers)
    # response.raise_for_status()
    print(response.status_code)
    # assert (response.status_code == 201), 'cannot connect to server'
    return response.status_code


def remove_product_from_server(barcode, date, name, ID, URL):
    URL = URL + f"/{barcode}" + f"/{date}"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFTOKEN': '6S1eiOl9Kvu3MIIezl9EDYznqvILwaCRU9hNYkBVtu8Z0sH6NMTBkHp3ZAfrnqdS',
        'Authorization': 'Token 62aa1bd2271eedd587232a3259f262fa5b578d88'
    }
    print(URL)
    response = requests.delete(URL, headers=headers)
    print(response.status_code)
    return response.status_code


def insert_product(CH: CameraHandler, modality, ser):

    if not CH.cap.isOpened():
        print("In insert_product: Camera could not be accessed.")
        return -1
    
    return_code = CH.start(ser=ser, modality=modality) #returns a dictionary with the product data and the barcode

    return return_code
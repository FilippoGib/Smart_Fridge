
import requests
from datetime import datetime
from src.camera_hanlder import CameraHandler


ID = 1
URL = f"http://127.0.0.1:8000/api/fridges/{ID}/products"


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

    information = CH.start(ser=ser) #returns a dictionary with the product data and the barcode

    if not CH.cap.isOpened():
        print("In insert_product: Camera could not be accessed.")
        return -1
    
    if information == 0:
        return 0
    
    product_data = information["product_data"]
    barcode = information["barcode"]
    expiry_date = information["date"]

    if product_data and barcode and expiry_date:
            data_og = expiry_date
            data_tmp = datetime.strptime(data_og, "%d/%m/%Y")
            data_correct_format = data_tmp.strftime("%Y-%m-%d")
    
            print(f"The product is {product_data.get('name')}, the barcode is {barcode} and the expity date is {data_correct_format}")
            print("Next step: comunicate with the server")
            print(modality)
            if modality == " INSERTION":
                print("###################### MODALITY = INSERTION ######################")
                status_code = send_product_to_server(barcode, data_correct_format, product_data.get('name'), ID=ID, URL=URL)
                print("send_product_to_server() has been called!!!!!!!!!!!!!!!!")
                if(status_code == 201):
                    print("Product inserted successfully")
                    print("You can insert the next product")
                    return 0
                else:
                    print("Product could not be inserted")
                    print(f"status_code: {status_code}")
                    return -2
                
            elif modality == " EXTRACTION":
                print("###################### MODALITY = EXTRACTION ######################")
                status_code = remove_product_from_server(barcode, data_correct_format, product_data.get('name'), ID=ID, URL=URL)
                if status_code == 200:
                    print("Product removed successfully")
                    print("You can remove the next product")
                    return 0
                else:
                    print("Product could not be removed")
                    return -2
    
    else:
         print("Could not retrieve information")
         return -1

import requests
from datetime import datetime
from src.camera_hanlder import CameraHandler


ID = "2"
URL = f"http://127.0.0.1:8000/api/fridges/{ID}/products"

def send_product_to_server(barcode, date, name): #json format
    data = {
         "fridge": f"{ID}",
         "barcode": f"{barcode}",
         "expire_date": f"{date}",
         "name": f"{name}"
    }
    response = requests.post(URL, data, verify=False)
    # response.raise_for_status()
    print(response.status_code)
    # assert (response.status_code == 201), 'cannot connect to server'
    return response.status_code


def insert_product(CH: CameraHandler):

    information = CH.start() #returns a dictionary with the product data and the barcode

    if CH.is_graceful_exit:
         print('Graceful exit')
         return -2

    if not CH.cap.isOpened():
        print("In insert_product: Camera could not be accessed.")
        return -1
    
    product_data = information["product_data"]
    barcode = information["barcode"]
    expiry_date = information["date"]

    if product_data and barcode and expiry_date:
            data_og = expiry_date
            data_tmp = datetime.strptime(data_og, "%d/%m/%Y")
            data_correct_format = data_tmp.strftime("%Y-%m-%d")
    
            print(f"The product is {product_data.get('name')}, the barcode is {barcode} and the expity date is {data_correct_format}")
            print("Next step: sending data to the server")
            status_code = send_product_to_server(barcode, data_correct_format, product_data.get('name'))
            print("sende_product_to_server() has been called!!!!!!!!!!!!!!!!")
            if(status_code == 201):
                print("Product inserted successfully")
                print("You can insert the next product")
                return 0
            else:
                print("Product could not be inserted")
                print(f"status_code: {status_code}")
                return -2
    else:
         print("CameraHandler.start() failed")
         return -1
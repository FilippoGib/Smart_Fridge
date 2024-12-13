from src.camera_hanlder import CameraHandler
from src.readeroptimazed import ExpirationDateReader
from src.external_fridge_monitor import ExternalFridgeMonitor
from utility.utils import send_product_to_server
from datetime import datetime
import threading


def insert_products():
    CH = CameraHandler()

    #TODO: 

    information = CH.start()

    product_data = information["product_data"]
    barcode = information["barcode"]

    if product_data and barcode:
        EDR = ExpirationDateReader(use_gpu=False)
        expiry_date = EDR.read_date_from_camera()
        if expiry_date and product_data and barcode:

            data_og = expiry_date
            data_tmp = datetime.strptime(data_og, "%d/%m/%Y")
            data_correct_format = data_tmp.strftime("%Y-%m-%d")
    
            print("I got both data and date!")
            print(f"The product is {product_data.get('name')}, the barcode is {barcode} and the expity date is {data_correct_format}")

            send_product_to_server(barcode, data_correct_format, product_data.get('name'))

def monitoring_fridge():
    fm = ExternalFridgeMonitor()
    fm.monitoring_loop()


def main():
    #concurrently start two threads to 
    monitoring_thread = threading.Thread(target=monitoring_fridge)
    inserting_thread = threading.Thread(target=insert_products)
    
    monitoring_thread.start()

    #TODO: when the switch is triggered the thread to insert products starts 
    inserting_thread.start()

    monitoring_thread.join()
    inserting_thread.join()

if __name__ == "__main__":
    main()
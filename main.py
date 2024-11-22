from src.camera_hanlder import CameraHandler
from src.readeroptimazed import ExpirationDateReader
from utility.camera_handler_utils import send_product_to_server
from datetime import datetime

def main():
    CH = CameraHandler()

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

    # send_product_to_server("9090929920", "2024-11-23", "Macachi")
    

if __name__ == "__main__":
    main()
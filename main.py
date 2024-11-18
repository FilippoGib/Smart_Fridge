from src.camera_hanlder import CameraHandler
from src.readeroptimazed import ExpirationDateReader

def main():
    CH = CameraHandler()
    product_data = CH.start()
    if product_data:
        EDR = ExpirationDateReader(use_gpu=False)
        expiry_date = EDR.read_date_from_camera()
    if expiry_date and product_data:
        print("I got both data and date!")
        print(f"The product is {product_data.get('name')} and the expity date is {expiry_date}")

if __name__ == "__main__":
    main()
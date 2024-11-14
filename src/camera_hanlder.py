import cv2
import numpy as np
from pyzbar.pyzbar import decode
import requests
import os

from utility.camera_handler_utils import preprocess_image, decode_frame_barcode


os.environ["QT_QPA_PLATFORM"] = "xcb" #non so se serve
ip_address = "https://172.20.10.6:4343/video" #cambiare secondo necessità, devi essere sullo stesso wi-fi del telefono, no eduroam


class CameraHandler():
    
    #constructor
    def __init__(self):
        self.cap = cv2.VideoCapture(ip_address)

        self.start()


    def start(self):
        if not self.cap.isOpened():
            print("ERROR: Camera could not be accessed.")
            return None

        print("Camera acquired successfully")

        product_data = self.detecting_product_data()
        
        if product_data:
            print("Product data: ", product_data.get('name'))
        else:
            print("Product data could not be retreived")
        
        expiry_date = self.detecting_product_expiry_date()

        if expiry_date:
            print("Product expiry date: ", expiry_date)
        else:
            print("No date found, it's alright")
        

        print("Execution Terminated Successfully!")



    def detecting_product_data(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("ERROR: Frame capture failed.")
                break

            # Apply preprocessing before decoding
            processed_frame = preprocess_image(frame)

            cv2.imshow('Processed Camera Feed', processed_frame)
            product_data = decode_frame_barcode(processed_frame)
            if product_data:
                self.cap.release()
                cv2.destroyAllWindows()
                return product_data

            # Delay to reduce frequency of "not decoded" message
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting capture.")
                break

        self.cap.release()
        cv2.destroyAllWindows()
        return None
    

    def detecting_product_expiry_date(self):
        return False


    



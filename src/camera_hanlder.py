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
        #self.cap = cv2.VideoCapture('/dev/video4')

        print("Camera Hadler ready to start!")
        #self.start()


    def start(self):
        if not self.cap.isOpened():
            print("ERROR: Camera could not be accessed.")
            return None

        print("Camera acquired successfully")

        information = self.detecting_product_data()

        product_data = information["product_data"]
        barcode = information["barcode"]
        
        if product_data and barcode:
            print("Product data: ", product_data.get('name'))
            print("Barcode: ", barcode)
            return {"product_data": product_data, "barcode": barcode}
        else:
            print("Product data could not be retreived")
            return None


    def detecting_product_data(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print("ERROR: Frame capture failed.")
                break

            # Apply preprocessing before decoding
            processed_frame = preprocess_image(frame)

            cv2.imshow('Processed Camera Feed', processed_frame)
            information = decode_frame_barcode(processed_frame)
            if information:
                self.cap.release()
                cv2.destroyAllWindows()
                return information

            # Delay to reduce frequency of "not decoded" message
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting capture.")
                break

        self.cap.release()
        cv2.destroyAllWindows()
        return None
    



    



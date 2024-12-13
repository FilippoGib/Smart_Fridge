from src.camera_hanlder import CameraHandler
from src.readeroptimazed import ExpirationDateReader
from src.external_fridge_monitor import ExternalFridgeMonitor
from src.internal_fridge_monitor import InternalFridgeMonitor
import utility.camera_utils as camera_utils
from datetime import datetime
import threading


def monitoring_fridge_extern():
    fm = ExternalFridgeMonitor()
    fm.monitoring_loop()


def monitoring_fridge_intern():
    fm = InternalFridgeMonitor()
    fm.monitoring_loop()


def main():
    #concurrently start two threads to 
    external_thread = threading.Thread(target=monitoring_fridge_extern)
    internal_thread = threading.Thread(target=insert_products)
    
    external_thread.start()

    #TODO: when the switch is triggered the thread to insert products starts 
    internal_thread.start()

    external_thread.join()
    internal_thread.join()

if __name__ == "__main__":
    main()
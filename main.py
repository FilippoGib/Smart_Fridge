from src.external_fridge_monitor import ExternalFridgeMonitor
from src.internal_fridge_monitor import InternalFridgeMonitor
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
    #internal_thread = threading.Thread(target=monitoring_fridge_intern)
    
    external_thread.start()
    #internal_thread.start()

    external_thread.join()

if __name__ == "__main__":
    main()
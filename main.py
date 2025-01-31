from src.external_fridge_monitor import ExternalFridgeMonitor
from utility.gps_utils import send_GPS_data_to_server

def monitoring_fridge_extern():
    fm = ExternalFridgeMonitor()
    GPS_data = fm.read_GPS()
    send_GPS_data_to_server(GPS_data=GPS_data)
    fm.monitoring_loop()


def main():

    monitoring_fridge_extern()   


if __name__ == "__main__":
    main()
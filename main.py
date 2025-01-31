from src.external_fridge_monitor import ExternalFridgeMonitor
from utility.gps_utils import send_GPS_data_to_server

def monitoring_fridge_extern():
    fm = ExternalFridgeMonitor()

    # start handling GPS data
    GPS_data = fm.read_GPS()
    send_GPS_data_to_server(GPS_data=GPS_data)
    # finished handling GPS data

    # starting to monitor the movement sensor
    fm.monitoring_loop()


def main():

    monitoring_fridge_extern()   


if __name__ == "__main__":
    main()
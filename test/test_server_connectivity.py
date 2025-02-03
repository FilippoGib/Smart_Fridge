from utility.monitor_utils import send_product_to_server, remove_product_from_server
from utility.gps_utils import send_GPS_data_to_server


def test_insertion(name, date, barcode, ID, URL):
    response = send_product_to_server(barcode=barcode, date=date, name=name, ID=ID, URL=URL)
    assert response == 201, "TEST: Product could not be inserted"

    response = remove_product_from_server(barcode=barcode, date=date, name=name, ID=ID, URL=URL)
    assert response == 200, "TEST: Product could not be removed"

    response = send_GPS_data_to_server({'latitude': 200.000000, 'longitude': 200.000000, 'satellites': 200, 'altitude': 200})

    if response not in (200, 201):
        raise AssertionError("TEST: GPS data could not be sent")



def main():
    name = "PROVAPROVAPROVAPROVA"
    date = "2024-12-16"
    barcode = "123456789"
    ID = 1
    URL = f"http://192.168.43.5:8080/api/fridges/{ID}/products" #change the IP address to the server's IP address

    test_insertion(name, date, barcode, ID=ID, URL=URL)
    


if __name__ == '__main__':
    main()
    print('All tests passed')

    
from utility.monitor_utils import send_product_to_server, remove_product_from_server


def test_insertion(name, date, barcode, ID, URL):
    response = send_product_to_server(barcode=barcode, date=date, name=name, ID=ID, URL=URL)
    assert response == 201, "Product could not be inserted"

    response = remove_product_from_server(barcode=barcode, date=date, name=name, ID=ID, URL=URL)
    assert response == 200, "Product could not be removed"


def main():
    name = "PROVAPROVAPROVAPROVA"
    date = "2024-12-16"
    barcode = "123456789"
    ID = 1
    URL = f"http://127.0.0.1:8000/api/fridges/{ID}/products" #change the IP address to the server's IP address

    test_insertion(name, date, barcode, ID=ID, URL=URL)
    


if __name__ == '__main__':
    main()
    print('All tests passed')

    
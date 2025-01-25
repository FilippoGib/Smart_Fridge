from utility.monitor_utils import send_product_to_server
import requests



def test(name, date, barcode, ID, URL):
    data = {
         "fridge": f"{ID}",
         "barcode": f"{barcode}",
         "expire_date": f"{date}",
         "name": f"{name}"
    }
    print(data)
    try:
        response = requests.post(URL, data, verify=False)
        response.raise_for_status()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
        
    status_code = response.status_code
    assert (status_code == 201), 'cannot connect to server'

if __name__ == '__main__':
    name = "test"
    date = "2024-12-16"
    barcode = "123456789"
    ID = "2"
    URL = f"http://127.0.0.1:8000/api/fridges/{ID}/products" #change the IP address to the server's IP address

    test(name, date, barcode, ID, URL)
    print('All tests passed')

    
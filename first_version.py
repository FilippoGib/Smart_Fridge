import cv2
import numpy as np
from pyzbar.pyzbar import decode
import requests
import os


ip_address = "https://172.20.10.7:4343/video"
os.environ["QT_QPA_PLATFORM"] = "xcb"


# to read barcodes from camera images
def capture_frames():
    cap = cv2.VideoCapture(ip_address)

    if not cap.isOpened():
        print("ERROR: Camera could not be accessed.")
        return None

    print("Camera acquired successfully")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("ERROR: Frame capture failed.")
            break

        # Apply preprocessing before decoding
        processed_frame = preprocess_image(frame)

        cv2.imshow('Processed Camera Feed', processed_frame)
        product_data = decoding(processed_frame)
        if product_data:
            cap.release()
            cv2.destroyAllWindows()
            return product_data

        # Delay to reduce frequency of "not decoded" message
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting capture.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return None


def preprocess_image(img):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Sharpen the image
    sharpened = cv2.addWeighted(gray, 1.5, blurred, -0.5, 0)
    
    # Apply adaptive thresholding to enhance barcode lines
    #thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Resize the image for better readability
    scale_percent = 100  # Increase the image size by 150%
    width = int(sharpened.shape[1] * scale_percent / 100)
    height = int(sharpened.shape[0] * scale_percent / 100)
    resized = cv2.resize(sharpened, (width, height), interpolation=cv2.INTER_LINEAR)

    return resized


def capture_image(image):
    return decoding(preprocess_image(cv2.imread(image)))


def find_product(barcode):
    # Request URL to OpenFoodFacts API
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 1:  # Status 1 means the product was found
            product = data['product']
            return {
                "name": product.get("product_name", "Not available"),
                "brand": product.get("brands", "Not available"),
                "categories": product.get("categories", "Not available"),
                "ingredients": product.get("ingredients_text", "Not available"),
                "nutrition": product.get("nutriments", "Not available"),
                "image": product.get("image_url", "Not available")
            }
        else:
            print("Product not found.")
            return None
    else:
        print(f"Request error: {response.status_code}")
        return None


def decoding(img):
    decoded_data = decode(img)
    if not decoded_data:
        print("No data in this frame")
        return None

    barcode = decoded_data[0].data.decode("utf-8")
    print('Barcode found: ' + barcode)
    product = find_product(barcode)
    return product


def main():
    data = capture_frames()
    # data = capture_image("images/parmalat.png")
    if data:
        print("Product data:", data.get('name'))
    else:
        print("Something went horribly wrong...")
        return
    print("Execution Terminated Successfully!")


if __name__ == "__main__":
    main()

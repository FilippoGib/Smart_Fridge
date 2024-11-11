import cv2
import numpy as np
from pyzbar.pyzbar import decode
import requests
import os

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
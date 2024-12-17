from src.camera_hanlder import CameraHandler

def main():
    CH = CameraHandler()
    product_data = CH.start()
    if product_data:
        print(f"The data i found is {product_data['product_data']}")


if __name__ == "__main__":
    main()
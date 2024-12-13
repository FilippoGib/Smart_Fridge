from src.date_reader import ExpirationDateReader

def main():
    EDR = ExpirationDateReader(use_gpu=False)
    date = EDR.read_date_from_camera()
    if date:
        print(f"The date is: {date}")


if __name__ == "__main__":
    main()
import serial
import json


# Set up the serial connection
arduino_port = "/dev/ttyUSB0"  # Replace with your Arduino's port (e.g., COM3 on Windows)
baud_rate = 9600


try:
    # Open the serial port
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    print(f"Connected to {arduino_port}")
except serial.SerialException:
    print(f"Error: Could not connect to {arduino_port}")
    exit()

while True:
    try:
        # Read a line of data from the Arduino
        raw_data = ser.readline().decode('utf-8').strip()
        
        if raw_data:
            # Parse the JSON data
            try:
                gps_data = json.loads(raw_data)
                print("GPS Data:")
                print(f"Latitude: {gps_data['latitude']}")
                print(f"Longitude: {gps_data['longitude']}")
                print(f"Satellites: {gps_data['satellites']}")
                print(f"Altitude: {gps_data['altitude']} meters")
                print("=========================")
            except json.JSONDecodeError:
                print("Received invalid JSON:", raw_data)

    except KeyboardInterrupt:
        print("Exiting...")
        ser.close()
        break

import serial
import serial.tools.list_ports
import utility.monitor_utils as monitor_utils
from src.camera_hanlder import CameraHandler
import threading
import time
import json
import cv2

threshold = 40

class ExternalFridgeMonitor():

	def __init__(self):
		self.portname = "/dev/ttyUSB0"  # Replace with your Arduino's port (e.g., COM3 or /dev/ttyUSB0)
		# potrebbe essere che se hai arduino ide aperto non riesci a comunicare in seriale perchè la porta è occupata
		self.baud_rate = 9600
		self.ser = None
		self.IS_CAMERA_OPEN = False
		self.COUNTER = 0
		self.stop_inserting_thread = threading.Event()  # Event to signal thread termination
		self.inserting_product_loop_thread = None
		self.modality = None
		self.setupSerial()


	def setupSerial(self):
		try:
			print ("connecting to " + self.portname)
			self.ser = serial.Serial(self.portname, baudrate=self.baud_rate, timeout=0)
		except serial.SerialException as e:
			self.ser = None
			print("Cannot connect to " + self.portname)
			print(f"Error: {e}")
			exit(1)


	def monitoring_loop(self):
		#infinite loop for serial managing
		#constantly monitor temperature and humidity of the fridge
		while (True):
			#look for a byte from serial
			if not self.ser is None:
				if self.ser.in_waiting > 0: #data available from the serial port
					#the message is ithe "HIGH, INSERTING" or "HIGH, EXTRACTION" or "LOW"
					input_message = self.ser.readline().decode('utf-8').strip().split(",") # data is ither LOW or HIGH
					data = input_message[0]
					if data == 'HIGH': # I know that I also received the message "INSERTING" or "EXTRACTION"
						if self.modality != input_message[1]: #I'm reading a different modality
							#kill the thread that is inserting the product
							if self.IS_CAMERA_OPEN:
								self.IS_CAMERA_OPEN = False
								self.stop_inserting_thread.set()
							self.modality = input_message[1]
							time.sleep(2)
						self.COUNTER = 0
						print('HIGH, ' + self.modality)
						if self.IS_CAMERA_OPEN == False:
							self.stop_inserting_thread.clear()  # Unset the stop signal
							#inizialize camera
							self.IS_CAMERA_OPEN = True
							#aggiungere la logica che legge lo stato dello switch se è IN o OUT
							self.inserting_product_loop_thread = threading.Thread(target=self.inserting_product_loop)
							self.inserting_product_loop_thread.start()
						else:
							#camera is already open
							print('CAMERA IS ALREADY OPEN')

					else: #I'm reading LOW
						if self.IS_CAMERA_OPEN:
							#LOGIC TO BE ADDED
							self.COUNTER += 1
							print(self.COUNTER)
							if self.COUNTER >= threshold:
								# kill the thread that is inserting the product
								self.IS_CAMERA_OPEN = False
								self.stop_inserting_thread.set()  # Set the stop signal
								print('Signal to kill current thread')
								if self.inserting_product_loop_thread is not None:
									self.inserting_product_loop_thread.join()
									self.inserting_product_loop_thread = None  # optional cleanup
								self.COUNTER = 0
						print('LOW')
		

	def inserting_product_loop(self):
		CH = CameraHandler(self.stop_inserting_thread)
		assert isinstance(CH, CameraHandler)
		#i want to create the camera handler object only once outside the inserting loop
		while not self.stop_inserting_thread.is_set() and CH.successfully_initialized:
			return_code = monitor_utils.insert_product(CH, modality=self.modality, ser = self.ser) # return = 0 success, return = -3 timeout, return = -2 server error, return = -1 camera error
			if return_code == 0: #success
				print(return_code)
				self.ser.write(b"s")
				continue
			elif return_code == -2:
				print("Server error")
				self.ser.write(b"e")
				continue
			elif return_code == -1: 
				print('camera error')
				self.ser.write(b"e")
				break			
			elif return_code == -3:
				print('Sensor movement timeout or switched modality')
				# break
		for i in range(50):
			self.ser.write(b"o")
		print("Thread stopped")


	def read_GPS(self):

		buffer = ""  # Buffer to store incoming data
		counter = 0

		while True:
			if self.ser.is_open:  # Check if the port is open
				
				raw_data = self.ser.read(self.ser.in_waiting or 1).decode('utf-8', errors='ignore')  # Read available bytes

				if not raw_data:
				    continue

				buffer += raw_data  # Append data to the buffer

				# Check if a full JSON object is present
				if "{" in buffer and "}" in buffer:
					start = buffer.find("{")  # Find first `{`
					end = buffer.rfind("}")  # Find last `}`
					json_data = buffer[start:end+1]  # Extract the JSON string

					try:
						parsed_data = json.loads(json_data)  # Parse JSON
						required_keys = {"latitude", "longitude", "satellites", "altitude"}

						if required_keys.issubset(parsed_data.keys()):
							counter += 1
							if counter >= 5:
								print("STOPPED")
								self.ser.write(b"STOP\n")
								return parsed_data

						buffer = ""  # Clear buffer after successful parsing
					except json.JSONDecodeError as e:
						print(f"Error parsing JSON: {e}")  # Handle incomplete JSON

			else:
				print("Serial port is not open")
				exit(1)








	
	


import serial
import serial.tools.list_ports
import utility.monitor_utils as monitor_utils
from src.camera_hanlder import CameraHandler
import threading
import time

threshold = 20

class ExternalFridgeMonitor():

	def __init__(self):
		self.portname = "/dev/ttyUSB0"  # Replace with your Arduino's port (e.g., COM3 or /dev/ttyUSB0)
		#potrebbe essere che se hai arduino ide aperto non riesci a comunicare in seriale perchè la porta è occupata
		self.baud_rate = 9600
		self.ser = None
		self.IS_CAMERA_OPEN = False
		self.COUNTER = 0
		self.setupSerial()
		self.CH = None


	def setupSerial(self):
		
		try:
			print ("connecting to " + self.portname)
			self.ser = serial.Serial(self.portname, baudrate=self.baud_rate, timeout=0)
		except:
			self.ser = None
			print("Cannot connect to " + self.portname)
			exit(1)

	def monitoring_loop(self):
		#infinite loop for serial managing
		#constantly monitor temperature and humidity of the fridge
		while (True):
			#look for a byte from serial
			if not self.ser is None:
				if self.ser.in_waiting > 0: #data available from the serial port
					data = self.ser.readline().decode('utf-8').strip()
					if data == 'HIGH':
						self.COUNTER = 0
						print('HIGH')
						if self.IS_CAMERA_OPEN == False:
							#inizialize camera
							self.CH = CameraHandler()
							self.IS_CAMERA_OPEN = True
							#aggiungere la logica che legge lo stato dello switch se è IN o OUT
							inserting_product_loop_thread = threading.Thread(target=self.inserting_product_loop, args=(self.CH, ))
							inserting_product_loop_thread.start()
						else:
							#camera is already open
							print('CAMERA IS ALREADY OPEN')
							
					else: #I'm reading LOW
						if self.IS_CAMERA_OPEN:
							#LOGIC TO BE ADDED
							self.COUNTER += 1
							print(self.COUNTER)
							if self.COUNTER >= threshold:
								self.CH.graceful_exit()
								self.COUNTER = 0
								self.IS_CAMERA_OPEN = False
						print('LOW')
		

	def inserting_product_loop(self, CH: CameraHandler):
		assert isinstance(CH, CameraHandler)
		while True:
			return_code = monitor_utils.insert_product(CH)
			if return_code == 0: #success
				print(return_code)
				continue
			elif return_code == -2: #graceful exit
				print("Server error")
				continue
			elif return_code == -1: 
				print('camera error')
				CH.graceful_exit()						
					


	



	
	


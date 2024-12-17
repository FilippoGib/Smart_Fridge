import serial
import serial.tools.list_ports
import utility.monitor_utils as monitor_utils
from src.camera_hanlder import CameraHandler
import threading


class ExternalFridgeMonitor():

	def __init__(self):
		self.portname = "/dev/ttyUSB0"  # Replace with your Arduino's port (e.g., COM3 or /dev/ttyUSB0)
		#potrebbe essere che se hai arduino ide aperto non riesci a comunicare in seriale perchè la porta è occupata
		self.baud_rate = 9600
		self.ser = None
		self.IS_CAMERA_OPEN = False
		self.setupSerial()


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

				if self.ser.in_waiting > 0:
					#data available from the serial port
					data = self.ser.readline().decode('utf-8').strip()
					CH = None
					if data == 'HIGH':
						print('HIGH')
						if self.IS_CAMERA_OPEN == False:
							#inizialize camera
							CH = CameraHandler()
							self.IS_CAMERA_OPEN = True
							print('CAMERA IS ALREADY OPEN')
							#aggiungere la logica che legge lo stato dello switch se è IN o OUT
							inserting_product_loop_thread = threading.Thread(target=self.inserting_product_loop, args=(CH, ))
							inserting_product_loop_thread.start()
						else:
							#camera is already open
							pass
					else:
						# #the sensor is not percieving movement
						# if ... : #the sensor hasn't percieved any movement in a while (tot time)
						# 	#turn camera off
						# 	CH.graceful_exit()
						print('LOW')
		

	def inserting_product_loop(self, CH: CameraHandler):
		assert isinstance(CH, CameraHandler)
		while True:
			return_code = monitor_utils.insert_product(CH)
			if return_code == 0: #success
				print(return_code)
			else: 
				print('something went wrong')
				return return_code						
					


	



	
	


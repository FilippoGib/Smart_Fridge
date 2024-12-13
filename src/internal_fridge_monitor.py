import serial
import serial.tools.list_ports

class InternalFridgeMonitor():

	def __init__(self):
		self.portname = "COM3"  # Replace with your Arduino's port (e.g., COM3 or /dev/ttyUSB0)
		self.baud_rate = 9600
		self.ser = None
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
					if data == 'HIGH':
						#the movement sensor has been triggered so I have to turn the camera on
						pass
					else:
						#the sensor is not percieving movement
						if ... : #the sensor hasn't percieved any movement in a while (tot time)
							#turn camera off
							pass
						
					


	



	
	


import bluetooth
import pigpio
import json

'''
This module serves as a Bluetooth Server. This class
handles all of the logic on the server side of things.
'''

class BtServer:
	'''
	This is the only class in this file. It sets up all of
	the control pins, binds to the controller, and handles
	inputs
	'''
	def __init__(self):
		# Setup pins
		self.SPEED_PIN = 21
		self.LATERAL_PIN = 20

		# Setup commands
		self.UPDATE_SPEED = "s"
		self.UPDATE_DIRECTION = "d"
		self.READY_FOR_UPDATE = "rfu"

		# Intialize GPIO
		self.pi = pigpio.pi()

		# Creating Socket Bluetooth RFCOMM communication
		self.server = self.create_bt_server()

	def create_bt_server(self):
		'''
		This method creates the Bluetooth connection
		and opens a socket.

		Code for this function and the next was found here:
		https://electronicshobbyists.com/controlling-gpio-through-android-app-over-bluetooth-raspberry-pi-bluetooth-tutorial/
		'''
		server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		host = ""
		port = 1 # Raspberry Pi uses port 1 for Bluetooth communication
		print('Bluetooth Socket Created')
		
		try:
			server.bind((host, port))
			print("Bluetooth Binding Completed")
		except Exception as e:
			print("Bluetooth Binding Failed")
		
		server.listen(1) # One connection at a time
		return server
		
	def start_listening(self):
		'''
		This method connects to the phone
		'''
		# Server accepts the clients request and assigns a mac address. 
		self.client, address = self.server.accept()
		print("Connected To", address)
		print("Client:", self.client)
		self.client.send(self.READY_FOR_UPDATE)

		while True:
			try:
        		# Receivng the data. 
				data = self.client.recv(1024).decode("utf-8") # 1024 is the buffer size.
				parsed_data = json.loads(data)
				if(parsed_data['e'] == self.UPDATE_SPEED):
					self.update_speed(int(parsed_data['v']))
				elif(parsed_data['e'] == self.UPDATE_DIRECTION):
					self.update_direction(int(parsed_data['v']))
				else:
					print("The JSON sent was invalid")
				self.client.send(self.READY_FOR_UPDATE)

			except json.decoder.JSONDecodeError as e:
				print(f'There was an issue parsing json. Skipping that value. {e} ' + str(parsed_data))

			except Exception as e:
				print(f'There was an issue receiving commands from the receiver - {e}')
				self.client.close()
				self.server.close()
				self.pi.set_servo_pulsewidth(self.SPEED_PIN, 0)
				self.server = self.create_bt_server()
				self.start_listening()

	def update_speed(self, value):
		'''
		This handles the speed using a linear equation
		'''
		slope = 10
		y_intercept = 1000
		pwm_value = slope * value + y_intercept
		self.pi.set_servo_pulsewidth(self.SPEED_PIN, pwm_value)

	def update_direction(self, value):
		'''
		This handles the speed using a linear equation
		'''
		slope = -3.8
		y_intercept = 2100
		pwm_value = slope * value + y_intercept
		self.pi.set_servo_pulsewidth(self.LATERAL_PIN, pwm_value)

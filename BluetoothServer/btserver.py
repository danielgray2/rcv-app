# Importing the Bluetooth Socket library
import bluetooth

# Importing the GPIO library to use the GPIO pins of Raspberry pi
import RPi.GPIO as GPIO

class BtServer:
	def __init__(self):
		# Setup pins
		self.FORWARD_PIN = 40
		self.BACKWARD_PIN = 38
		self.LEFT_PIN = 13
		self.RIGHT_PIN = 15

		# Setup commands
		self.MOVE_FORWARD = "moveForward"
		self.STOP_MOVE_FORWARD = "stopMoveForward"
		self.MOVE_BACKWARD = "moveBackward"
		self.STOP_MOVE_BACKWARD = "stopMoveBackward"
		self.TURN_LEFT = "turnLeft"
		self.STOP_TURN_LEFT = "stopTurnLeft"
		self.TURN_RIGHT = "turnRight"
		self.STOP_TURN_RIGHT = "stopTurnRight"
		self.SHUTDOWN = "shutdown"

		# Intialize GPIO
		GPIO.setmode(GPIO.BOARD)
		self.pin_array = [self.FORWARD_PIN, self.BACKWARD_PIN, self.LEFT_PIN, self.RIGHT_PIN]
		GPIO.setup(self.pin_array, GPIO.OUT)

		# Creating Socket Bluetooth RFCOMM communication
		self.server = self.create_bt_server()
	
	def create_bt_server(self):
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
		# Server accepts the clients request and assigns a mac address. 
		self.client, address = self.server.accept()
		print("Connected To", address)
		print("Client:", self.client)

		# Create a dictionary we use as a switch statement
		switch_dict = self.create_switch_dict()

		try:
			while True:
        		# Receivng the data. 
				data = self.client.recv(1024).decode("utf-8") # 1024 is the buffer size.
				print(data)

				# Get the function and execute it
				func = switch_dict.get(data, lambda: "Invalid input")
				func()
				
		except Exception as e:
			print(f'There was an issue receiving commands from the receiver - {e}')
			self.stop_pins()

	def create_switch_dict(self):
		return {	
			self.MOVE_FORWARD: self.move_forward,
			self.STOP_MOVE_FORWARD: self.stop_move_forward,
			self.MOVE_BACKWARD: self.move_backward,
			self.STOP_MOVE_BACKWARD: self.stop_move_backward,
			self.TURN_LEFT: self.turn_left,
			self.STOP_TURN_LEFT: self.stop_turn_left,
			self.TURN_RIGHT: self.turn_right,
			self.STOP_TURN_RIGHT: self.stop_turn_right,
			self.SHUTDOWN: self.shutdown
		}

	def move_forward(self):
		GPIO.output(self.FORWARD_PIN, True)

	def stop_move_forward(self):
		GPIO.output(self.FORWARD_PIN, False)

	def move_backward(self):
		GPIO.output(self.BACKWARD_PIN, True)

	def stop_move_backward(self):
		GPIO.output(self.BACKWARD_PIN, False)

	def turn_right(self):
		GPIO.output(self.RIGHT_PIN, True)

	def stop_turn_right(self):
		GPIO.output(self.RIGHT_PIN, False)

	def turn_left(self):
		GPIO.output(self.LEFT_PIN, True)

	def stop_turn_left(self):
		GPIO.output(self.LEFT_PIN, False)
	
	def shutdown(self):
		# Making all the output pins LOW
		GPIO.cleanup()

		# Closing the client and server connection
		self.client.close()
		self.server.close()
	
	def stop_pins(self):
		for pin in self.pin_array:
			GPIO.output(pin, False)

import bluetooth
import RPi.GPIO as GPIO
import pigpio
import json

class BtServer:
	def __init__(self):
		# Setup pins
		self.SPEED_PIN = 21
		self.LATERAL_PIN = 20

		# Setup commands
		self.UPDATE_SPEED = "s"
		self.UPDATE_DIRECTION = "d"
		self.SHUTDOWN = "shutdown"
		self.READY_FOR_UPDATE = "rfu"

		# Intialize GPIO
		self.pi = pigpio.pi()

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
		self.client.send(self.READY_FOR_UPDATE)

		while True:
			try:
        		# Receivng the data. 
				data = self.client.recv(1024).decode("utf-8") # 1024 is the buffer size.
				print("Here is the data: " + str(data))
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
		#slope = -5.85
		#y_intercept = 1455
		#pwm_value = slope * value + y_intercept
		#self.pi.set_servo_pulsewidth(self.SPEED_PIN, pwm_value)
		slope = 10
		y_intercept = 1000
		pwm_value = slope * value + y_intercept
		self.pi.set_servo_pulsewidth(self.SPEED_PIN, pwm_value)
		print("Here is the PWM: " + str(pwm_value))

	def update_direction(self, value):
		#slope = 0.0388
		#y_intercept = 7
		#processed_value = abs((value - 50)) % 100
		#print("Here is the processed value: " + str(processed_value))
		#if(value > 50):
		#	processed_value = -processed_value
		#pwm_value = slope * processed_value + y_intercept
		##print("Here is the pwm_value: " + str(pwm_value))
		#self.lateral_pwm.ChangeDutyCycle(pwm_value)
		slope = -3.8
		y_intercept = 2100
		pwm_value = slope * value + y_intercept
		self.pi.set_servo_pulsewidth(self.LATERAL_PIN, pwm_value)
		print("RAW_VALUE: " + str(value))
		print("PWM_VALUE: " + str(pwm_value))
	
	def shutdown(self):
		# Making all the output pins LOW
		GPIO.cleanup()

		# Closing the client and server connection
		self.client.close()
		self.server.close()
	
	def stop_pins(self):
		for pin in self.pin_array:
			GPIO.output(pin, False)

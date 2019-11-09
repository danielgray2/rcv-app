# Importing the Bluetooth Socket library
import bluetooth
# Importing the GPIO library to use the GPIO pins of Raspberry pi
import RPi.GPIO as GPIO

FORWARD_PIN = 40
BACKWARD_PIN = 38
LEFT_PIN = 13
RIGHT_PIN = 15


MOVE_FORWARD = "moveForward"
STOP_MOVE_FORWARD = "stopMoveForward"
MOVE_BACKWARD = "moveBackward"
STOP_MOVE_BACKWARD = "stopMoveBackward"
TURN_LEFT = "turnLeft"
STOP_TURN_LEFT = "stopTurnLeft"
TURN_RIGHT = "turnRight"
STOP_TURN_RIGHT = "stopTurnRight"

GPIO.setmode(GPIO.BOARD)
GPIO.setup([FORWARD_PIN, BACKWARD_PIN, LEFT_PIN, RIGHT_PIN], GPIO.OUT)
host = ""
port = 1	# Raspberry Pi uses port 1 for Bluetooth Communication
# Creaitng Socket Bluetooth RFCOMM communication
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print('Bluetooth Socket Created')
try:
    server.bind((host, port))
    print("Bluetooth Binding Completed")
except:
    print("Bluetooth Binding Failed")
server.listen(1) # One connection at a time
# Server accepts the clients request and assigns a mac address. 
client, address = server.accept()
print("Connected To", address)
print("Client:", client)
try:
    while True:
        # Receivng the data. 
        data = client.recv(1024).decode("utf-8") # 1024 is the buffer size.
        print(data)
	
        if data == MOVE_FORWARD:
            GPIO.output(FORWARD_PIN, True)
            print("Did we actually come here")
            send_data = "Moving forward "
        elif data == STOP_MOVE_FORWARD:
            GPIO.output(FORWARD_PIN, False)
            send_data = "Stopped moving forward "
        elif data == MOVE_BACKWARD:
            print("Did we actually come to moving backward")
            GPIO.output(BACKWARD_PIN, True)
            send_data = "Moving backward "
        elif data == STOP_MOVE_BACKWARD:
            GPIO.output(BACKWARD_PIN, False)
            send_data = "Stopped moving backward "
        elif data == TURN_RIGHT:
            GPIO.output(RIGHT_PIN, True)
            send_data = "Turning right "
        elif data == STOP_TURN_RIGHT:
            GPIO.output(RIGHT_PIN, False)
            send_data = "Stopped turning right "
        elif data == TURN_LEFT:
            GPIO.output(LEFT_PIN, True)
            send_data = "Turning left "
        elif data == STOP_TURN_LEFT:
            GPIO.output(LEFT_PIN, False)
            send_data = "Stopped turning left "
        # Sending the data.
        client.send(send_data) 
except:
    # Making all the output pins LOW
    GPIO.cleanup()
    # Closing the client and server connection
    client.close()
    server.close()

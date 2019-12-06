from btserver import BtServer
import time

'''
This is the main function that is
called and runs the code
'''

if __name__ == "__main__":
	btServer = BtServer()
	btServer.start_listening()

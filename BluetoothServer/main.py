from btserver import BtServer
import time

if __name__ == "__main__":
	#time.sleep(15)
	btServer = BtServer()
	btServer.start_listening()

import socket
import sys
import threading
 
ip = '192.168.43.160'   
PORT = 8888 
BUF_LEN = 15
 
def from_android():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = (ip, PORT)
	print("android socket listening...")
	sock.bind(server_address)
	sock.listen(1)

	try:
		
		while True:	
			client, address = sock.accept()
			#print("Android Connected")

			data = client.recv(BUF_LEN)
			
			if not data:
				break

			data = data[:-1]
			print(data.decode())
	
	except:
		print("close Android")
		client.close()
		sock.close()
		exit(1)	

ANDROID = threading.Thread(target=from_android)

ANDROID.start()

ANDROID.join()


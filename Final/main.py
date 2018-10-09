import os
import socket
import sys
import threading
import spidev

ip = '192.168.43.160'   
PORT = 8888 
BUF_LEN = 15

spi = spidev.SpiDev()
spi.open(3, 0)
spi.max_speed_hz = 1000000
 
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

			if(data.decode() == 'start'):
				#data.decode()
				to_arduino(data.decode())
				os.system("sudo python3 line_stream.py")

			# send data to arduino
			#to_arduino(data.decode())
		
	except:
		print("close Android")
		client.close()
		sock.close()
		exit(1)	

def to_arduino(msg):
	msglist = list()
	msglist = []

	i = 0
	for x in msg:
		msglist.insert(i, ord(x))
		i += 1

	msglist.insert(i, ord('\0'))
	spi.xfer(msglist)


ANDROID = threading.Thread(target=from_android)

ANDROID.start()

ANDROID.join()


import cv2
import socket
import sys
import spidev
import threading
from ctypes import *
from line import get_lane

width, height = 800, 600
ip = '192.168.43.160'

BUF_LEN = 15

global CAR_CENTER, curve
CAR_CENTER, curve = int(380), int(90)

global isDriving
isDriving = 0
#spi

spi = spidev.SpiDev()
spi.open(3,0)
spi.max_speed_hz = 1000000

# Create a TCP/IP socket
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
#server_address = (ip, 8888)
#print >>sys.stderr, 'starting up on %s port %s' % server_address
#sock.bind(server_address)

def from_android():
	global isDriving
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_address = (ip, 8888)
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
				isDriving = 1
				break

	except:
		print("close Android")
		client.close()
		sock.close()
		exit(1)

def from_YOLO():
	global isDriving
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_address = (ip, 8889)
	print("YOLO socket listening...")
	sock.bind(server_address)
	sock.listen(1)
	
	try:
		
		while True:	
			client, address = sock.accept()

			data = client.recv(BUF_LEN)
			
			if not data:
				break

			data = data[:-1]
			print(data.decode())

	except:
		print("close YOLO")
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

def get_direction(point):
	global curve
	
	try:
		x_point = int(point)
	except:
		return 

	if x_point >= CAR_CENTER - 25 and x_point <= CAR_CENTER + 25:
		to_arduino("a");
		print("straight")
#curve = 90
	elif CAR_CENTER >= x_point:
		to_arduino("b");
		print("left")
#if curve > 40 and curve < 140:
#curve-=2
	elif CAR_CENTER < x_point:
		to_arduino("c");
		print("right")
#if curve > 40 and curve < 140:
#curve+=2

#cap = cv2.VideoCapture('videoplayback.mp4')
#cap = cv2.VideoCapture('challenge_video.mp4')

def main():
	cap = cv2.VideoCapture(1)
	print(cap.isOpened())
	from_android()

	if(isDriving == 1):

		while cap.isOpened():

			ret, frame = cap.read()
			frame = cv2.resize(frame, (width, height))


			try:
				frame, point = get_lane(frame)

				print("point, ", point)

				if point == -1:
					print("no left no right")
				elif point == -2:
					to_arduino("b");
		#if curve > 40 and curve < 140:
			
		#curve-=2
		#to_arduino(str(curve))
					print("no left")
				elif point == -3:
					to_arduino("c");
		#			if curve > 40 and curve < 140:
		#curve+=2
		#to_arduino(str(curve))
					print("no right")
				else:
		#		print("left and right")
					get_direction(point)
		#to_arduino(direction)
		#	print(point, ', ', curve)
		#to_arduino(str(curve))

			except:
				print("error")
				pass

			cv2.imshow('0825', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		cv2.destroyAllWindows()
		cap.release()

MAIN = threading.Thread(target=main)
YOLO = threading.Thread(target=from_YOLO)
YOLO.start()
MAIN.start()
YOLO.join()
MAIN.join()

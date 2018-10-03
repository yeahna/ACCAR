import cv2
import socket
import sys
import spidev
from ctypes import *
from line import get_lane

width, height = 800, 600
ip = '192.168.43.160'

global CAR_CENTER, curve
CAR_CENTER, curve = int(400), int(90)

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

	if x_point >= CAR_CENTER - 50 and x_point <= CAR_CENTER + 50:
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
cap = cv2.VideoCapture('challenge_video.mp4')
#cap = cv2.VideoCapture(1)
print(cap.isOpened())

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

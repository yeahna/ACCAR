import cv2
import socket
import sys
import spidev
from ctypes import *
from line_test2 import get_lane

width, height = 800,600
ip = '192.168.43.160'

global CAR_CENTER, curve
CAR_CENTER, curve = int(400), int(90)

#spi

spi = spidev.SpiDev()
spi.open(3,0)
spi.max_speed_hz = 1000000

def to_arduino(msg):
	msglist = list()
	msglist = []

	i = 0
	for x in msg:
		msglist.insert(i, ord(x))
		i += 1

	msglist.insert(i, ord('\0'))
	print(msg, " : ", msglist)
	spi.xfer(msglist)

def get_direction(point):
	global curve
	
	try:
		x_point = int(point)
	except:
		return 

	if x_point >= CAR_CENTER - 30 and x_point <= CAR_CENTER + 30:
		curve = 90
	elif CAR_CENTER >= x_point:
		if curve > 40 and curve < 140:
			curve-=2
	elif CAR_CENTER < x_point:
		if curve > 40 and curve < 140:
			curve+=2

#cap = cv2.VideoCapture('challenge_video.mp4')
#cap = cv2.VideoCapture('videoplayback.mp4')
cap = cv2.VideoCapture(1)

#width = cap.set(3,1280)
#height = cap.set(4,720)

print(cap.isOpened())

while cap.isOpened():

	ret, frame = cap.read()
	frame = cv2.resize(frame, (width, height))


	try:
		frame, point = get_lane(frame)

		if point == -1:
			print("no left no right")
		elif point == -2:
			if curve > 40 and curve < 140:
				curve-=2
				to_arduino(str(curve))
				print("no left")
		elif point == -3:
			if curve > 40 and curve < 140:
				curve+=2
				to_arduino(str(curve))
				print("no right")
		else:
			print("left and right")
			get_direction(point)
#to_arduino(direction)
			print(point, ', ', curve)
			to_arduino(str(curve))


	except:
		print("error")
		pass

	cv2.imshow('0825', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()
cap.release()

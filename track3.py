from collections import deque
import numpy as np
#import argparse
import cv2
import serial
from serial import Serial
import imutils
import time

arduino = serial.Serial('/dev/ttyUSB0', 115200,timeout=0)  
arduino.flush()					    
x_s=0
y_s=0
r_s=0
cap = cv2.VideoCapture(0)

time.sleep(5)

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points

greenLower = np.array([30, 1, 95 ])
greenUpper = np.array([30, 255, 255])


pts = deque(maxlen=64)
fo = cv2.FONT_HERSHEY_DUPLEX
w = (200,200,0)


# keep looping
while True:
	ret,img = cap.read(0)
	img = imutils.resize(img, width=320)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y),radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		if radius > 0:
			cv2.circle(mask, (int(x), int(y)), 5,(255, 0, 255), 2)
			cv2.putText(mask,"detected",(30,30),fo,1,w,2)
	if len(cnts) == 0:
		ada_color = 0
		x = 0
		y = 0
		
	x_s = x
	y_s = y + 500

	pts.appendleft(center)
	cv2.imshow("Frame", mask)
	cv2.imshow("img", img)
	data = str("%d %d\n") % (x_s, y_s)
	print ("detect: %d %d" % (x, y))	
	arduino.write(data.encode())   
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

#Frame cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()

	

#from collections import deque
import numpy as np
#import argparse
import cv2
#import serial
#from serial import Serial
import imutils
import time

#arduino = serial.Serial('/dev/ttyUSB0', 115200,timeout=0)  
#arduino.flush()					    
x_s=0
y_s=0
r_s=1
cap = cv2.VideoCapture(0)

time.sleep(5)

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points

greenLower = np.array([160, 48, 30 ])
greenUpper = np.array([170, 255, 255])


#pts = deque(maxlen=64)
fo = cv2.FONT_HERSHEY_DUPLEX
w = (200,200,0)


# keep looping
while True:
	ret,img = cap.read(0)
	img = imutils.resize(img, width=320)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y),radius) = cv2.minEnclosingCircle(c)
		#M = cv2.moments(c)
		if radius > 0:
			cv2.circle(mask, (int(x), int(y)), 5,(255, 0, 255), 2)
			cv2.putText(mask,"detected",(30,30),fo,1,w,2)

	
			if x < 100:
				cv2.putText(mask,"kanan",(30,60),fo,1,w,2) #aslinya 'kiri', berhubung kameranya menghadap depan maka di reverse
				data = 1
				#arduino.write(data)
	
			if x >= 100 and x < 200:
				cv2.putText(mask,"tengah",(30,60),fo,1,w,2) 
				data = str("2")
				#arduino.write(data.encode())

	
			if x >= 200 and x < 320:
				cv2.putText(mask,"kiri",(30,60),fo,1,w,2) #aslinya 'kanan', berhubung kameranya menghadap depan maka di reverse
				data = str("3")
				#arduino.write(data.encode())

		else:
			data = str("0")
			#arduino.write(data.encode())
			
	if len(cnts) == 0:
		ada_color = 0
		x = 0
		y = 0
		
	#x_s = x
	#y_s = y 

	fps = cap.get(cv2.CAP_PROP_FPS)
	afs = str("Fps {0}".format(fps))
	cv2.putText(img,afs,(10,10),fo,0.5,w)
	#pts.appendleft(center)
	cv2.imshow("Frame", mask)
	cv2.imshow("img", img)
	#data = str("%d %d\n") % (x_s, y_s)
	print ("detect: %d %d" % (x, y))	
	#arduino.write(data.encode())   
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break

#Frame cleanup the camera and close any open windows
cap.release()
cv2.destroyAllWindows()



import cv2
import numpy as np 
import time 

cap = cv2.VideoCapture('video.mp4')

# giving the camera time to warm up 
time.sleep(1)
count = 0 
background = 0 

for i in range(60):
	ret , background = cap.read()
	if not ret :
		continue 

background = np.flip(background , axis = 1)

while cap.isOpened() :
	ret , img = cap.read()

	if not ret :
		break 

	count += 1
	img = np.flip(img , axis = 1)

	# converting BGR to HSV 
	hsv = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)

	# lower and upper red for mask1
	lower_red = np.array([0,120,70])
	upper_red = np.array([10,255,255]) 
	# values is for red colour Cloth
	mask1 = cv2.inRange(hsv, lower_red,upper_red)
    
	# lower and upper red for mask2
	lower_red = np.array([170,120,70])
	upper_red =  np.array([180,255,255])
	mask2 = cv2.inRange(hsv,lower_red,upper_red)

	mask1 = mask1 +  mask2 

	# morphological operations just removes unnesccessary details that appear on the screen 
	mask1 = cv2.morphologyEx(mask1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8), iterations = 2)
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE,np.ones((3,3),np.uint8), iterations = 1)

	mask2 =cv2.bitwise_not(mask1)

	# combining the mask and showing them in one frame 
	res1 = cv2.bitwise_and(background , background , mask = mask1)
	res2 = cv2.bitwise_and(img , img , mask = mask2)
	final_output = cv2.addWeighted(res1 , 1 , res2 , 1 , 0)
	cv2.imshow('Invisible Cloak' , final_output)

	k = cv2.waitKey(1)
	if k == 27 :
		cap.release()
		cv2.destroyAllWindows()
		quit()
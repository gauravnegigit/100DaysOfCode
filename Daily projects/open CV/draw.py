import cv2
import numpy as np 

drawing = False       # turned into true while dragging the mouse   
mode = True 		  # if tRue , then it will draw the rectangle 
px , py = -1 , -1 


def draw(event , x , y , flag , param):
	global mode , drawing , px , py 

	if event == cv2.EVENT_LBUTTONDOWN :
		drawing = True 
		px , py = x, y 

	elif event == cv2.EVENT_MOUSEMOVE :
		if drawing :
			if mode :
				cv2.rectangle(img , (px , py) , (x , y) , (0 , 255 , 0) , 5)
				a = x 
				b = y 

				if not(a != x or b != y) :
					cv2.rectangle(img , (px , py) , (x , y) , (0 , 0 , 0) , -1)

			else :
				cv2.circle(img , (x , y) , 5 , (0 , 0 , 255) , -1)

	elif event == cv2.EVENT_LBUTTONUP :
		drawing = False 

		if mode : 
			cv2.rectangle(img, (px, py), (x, y), (0, 255, 0), 5)
		else :
			cv2.circle(img , (x , y) , 5 , (0 , 0 , 255) , - 1)


img = np.zeros((512 , 512 , 3) , np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image' , draw)

while True :
	cv2.imshow('image' , img)

	key = cv2.waitKey(1) & 0xFF

	if key == ord('m') :
		mode = not mode 

	elif key == 27 :
		break 

cv2.destroyAllWindows()
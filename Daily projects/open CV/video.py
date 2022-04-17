import numpy as np 
import cv2

cap = cv2.VideoCapture('coding-kira.mp4')

def main():
	global cap 

	while True :
		ret , frame = cap.read()
		width , height = int(cap.get(3)) , int(cap.get(4))
		
		try : 
			image = np.zeros(frame.shape , np.uint8)
			samller_frame = cv2.resize(frame , (0 , 0) , fx = 0.5 , fy = 0.5)

			image[:height//2 , :width//2] = cv2.rotate(samller_frame , cv2.cv2.ROTATE_180)
			image[height//2: , :width//2] = samller_frame
			image[:height//2 , width//2:] = cv2.rotate(samller_frame , cv2.cv2.ROTATE_180)
			image[height//2: , width//2:] = samller_frame

			cv2.imshow('frame' , image)

		except : 
			cap = cv2.VideoCapture('coding-kira.mp4')
			main()

		if cv2.waitKey(1) == ord('q') :
			quit()

if __name__ == '__main__':
 	main() 

cap.release()
cv2.destroyAllWindows()
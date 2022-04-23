import cv2 
import time 

cap = cv2.VideoCapture('walk.gif')

counter = 0 
run = True 
frames = []

while run :
	run , frame = cap.read()
	# appending the frame to the frames 
	frames.append(frame)

# last value in the video file would be None so we need to pop it from the list : frames
frames.pop()

#reversing the frames list 
frames = frames[::-1]

# looping through in frame 
def reverse_play():
	'''
	This function will be used for reverse plaing the video as an infinite loop 
	'''

	for frame in frames :
		cv2.imshow('frame' , frame)

		time.sleep(0.03)

		if cv2.waitKey(1) == ord('q'):
			cap.release()
			cv2.destroyAllWindows()
			quit()

	reverse_play()

if __name__ == '__main__' :
	 reverse_play()

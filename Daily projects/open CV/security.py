import cv2
import datetime
import time 

# importing libraries for sending gmail with attachment 

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

# time reocrding variables

detection = False 

detection_stopped_time = None  
timer_started  = False
min_time = 5

frame_size = (int(cap.get(3)) , int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mpv4")

def send_email(current_time):
    """
    This function will come in handy in sending the video as an attachment to the required gmail account 
    """

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    msg['From'] = 'sender_email_id'
      
    # storing the receivers email address 
    msg['To'] = "receiver_id"

    sender  , receiver = 'sender_email_id' , 'receiver_id'
      
    # storing the subject 
    msg['Subject'] = "Security camera"

    # attaching the body within the msg instance 
    msg.attach(MIMEText("" , 'plain'))

    filename  = str(current_time) + ".mp4"
    attachment = open(f'E:\\Python section\\Python modules\\openCV\\{current_time}.mp4', "rb")


    p = MIMEBase('application' , 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition' , "attachement; filename = filename")

    msg.attach(p)

    # creating SMTP session
    s = smtplib.SMTP('smtp.gmail.com' , 587)

    # start TLS for security
    s.starttls()
      
    # Authentication
    s.login(sender, "password")
      
    # Converts the Multipart msg into a string
    text = msg.as_string()
      
    # sending the mail
    s.sendmail(sender , receiver, text)
      
    # terminating the session
    s.quit()
    print('mail sended')


while True :
    current_time = 0 

    ret , frame = cap.read()
    gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) + len(bodies) > 0 : 
        if detection : 
            timer_started = False  

        else :
            detection = True 
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4" , fourcc , 20 , frame_size)

            try : 
                send_email(current_time)
            except :
                print('Please check your internet connection in order to send the email !')

            print("Recording started")

    elif detection :
        if timer_started :
            if time.time() - detection_stopped_time >= min_time :
                detection = False 
                timer_started  = False 
                video = out.release()

                print("Recording stopped")

        else :
            timer_started = True 
            detection_stopped_time = time.time()

    cv2.imshow('Camera' , frame)

    if cv2.waitKey(1) == ord('q') :
        quit()

cap.release()
cv2.destoryAllWindows()
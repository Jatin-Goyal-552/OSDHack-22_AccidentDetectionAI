import cv2
import pandas

import cv2
import torch
import warnings
warnings.filterwarnings("ignore")
import vonage
import time
from django.core.mail import send_mail
from django.conf import settings
import pusher
from .models import *
import numpy as np
import argparse
import os
import sys
from pathlib import Path
import numpy as np
import cv2
import torch
import torch.backends.cudnn as cudnn







def check(t1,img,model):
    results = model(img)
    results.print()
    dummy_array = np.array(results.xyxy[0])
    dummy_array = dummy_array.astype(int)
    dummy_array = dummy_array[dummy_array[:,0].argsort()]
    return detect(dummy_array,t1)    

def send_notification(id,flag):
    pusher_client = pusher.Pusher(
    app_id='1328110',
    key='4da6311b184ace45d1dc',
    secret='469709e6b17fadfab16f',
    cluster='ap2',
    ssl=True
    )
    if flag:
        notif = Notifications(notification="accident happened",lattitude=47.5,longitude=122.33,accepted=0)
        
        notif.save()
    if id==1:
        pusher_client.trigger('my-channel', 'my-event', {'message2': 'Urgent\n please send ambulance as soon as possible at xyz address.'})
    if id==2:
        pusher_client.trigger('my-channel', 'my-event', {'request': 'Request Sent'})
    return


def detect(boxes,t1):
    n = len(boxes)
    for i in range(n):
        x1,y1,w1,h1 = boxes[i][0],boxes[i][1],boxes[i][2],boxes[i][3]
        for j in range(i+1,n):
            x2,y2,w2,h2 = boxes[j][0],boxes[j][1],boxes[j][2],boxes[j][3]
            if x2<(w1):
                xmin = min(x1,x2)
                xmax = max(w1,w2)
                ymin = min(y1,y2)
                ymax = max(h1,h2)
                print(xmin,xmax,ymin,ymax)
                print((xmin>=t1[0] & t1[0]<=xmax) | (xmin>=t1[2] & t1[2]<=xmax))
                print((ymin>=t1[1] & t1[1]<=ymax) | (ymin>=t1[3] & t1[3]<=ymax))
                if ((xmin>=t1[0] & t1[0]<=xmax) | (xmin>=t1[2] & t1[2]<=xmax)) & ((ymin>=t1[1] & t1[1]<=ymax) | (ymin>=t1[3] & t1[3]<=ymax)):
                    # print("are you here")
                    return True


    return False
def send_message():
    client = vonage.Client(key="4627a3c9", secret="KAd19Rz2sQ7HM3Tc")
    sms = vonage.Sms(client)
    responseData = sms.send_message(
        {
            "from": "Jatin Goyal",
            "to": "918168991401",
            "text": "Urgent \n Accident happened at raj labadi. Please send ambulance as soon as possible. Google map link :- https://www.google.com/maps/search/?api=1&query=47.5%2C-122.3316393 ",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

    
def sendmail():
    hospital=Hospital.objects.all()
    print(hospital.values())
    gmail_list=[]
    for hos in hospital.values():
        gmail_list.append(hos['email'])
    gmail_list.append("sachinkhandelwal9413@gmail.com")
    print("gmail list",gmail_list)
    email_subject = "Urgent please send ambulance."
    email_body = "Accident happened at raj labadi please send ambulance as soon as possible. Google map link :- https://www.google.com/maps/search/?api=1&query=47.5%2C122.3316393 "
    # email="sachinkhandelwal9413@gmail.com"
    print(send_mail(email_subject, email_body,
                  settings.EMAIL_HOST_USER, gmail_list, fail_silently=False))
    return 

class streaming(object):
    def __init__(self):
        print("hello")
        self.flag=True
        self.video_capture = cv2.VideoCapture(0)
        # self.video_capture = cv2.VideoCapture("C:\\Users\\LENOVO\\Downloads\\accident3.mp4")
        self.model1=torch.hub.load('ultralytics/yolov5', 'custom', path='C:\\Users\\LENOVO\\projects\\Dot_Slash_Road_Safety\\AccidentDetection\\best (2).pt',device='cpu')
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:\\Users\\LENOVO\\projects\\Dot_Slash_Road_Safety\\AccidentDetection\\accident2.pt',device='cpu')
# model1 = torch.hub.load('ultralytics/yolov5', 'custom', path='C:\\Users\\hp\\Desktop\\accident.pt')

    def get_frame(self):
        ret, frame = self.video_capture.read()
        cv2.imwrite("image.jpg",frame)
        imgs = cv2.imread("image.jpg")
        results = self.model1(imgs)
        # results.show()
        get = results.print()
        # print(get)

        dummy_array = np.array(results.xyxy[0])
        dummy_array = dummy_array.astype(int)
        # results = self.model(imgs)
        # dummy_array = np.array(results.xyxy[0])
        # dummy_array = dummy_array.astype(int)
        # # print(dummy_array[0])
        # dummy_array = dummy_array[dummy_array[:,0].argsort()]
        # print(dummy_array[0])
        # result= detect(dummy_array,t1)
        # coordinates=[]
        # df=results.pandas().xyxy[0]
        # if df.shape[0]!=0:
        #     print("*"*80)
        #     # print(df.head())
        #     print("Accident Happened")
        #     for i in range(df.shape[0]):
        #         # print((df.loc[i]['xmin']),df.loc[i]['ymin'], df.loc[i]['xmax'],df.loc[i]['ymax'])
        #         frame = cv2.rectangle(frame, (int(df.loc[i]['xmin']),int(df.loc[i]['ymin'])), (int(df.loc[i]['xmax']),int(df.loc[i]['ymax'])), (0,0,255), 2)
        #     # coordinates.append(results.pandas().xyxy[0].iloc[:,:-3])
        #     print("*"*80)
        # print("*"*80)
        # print(results.pandas().xyxy[0].head())
        # print(results.pandas().xyxy[0].shape)
        # print("*"*80)
        # # frame=cv2.imread(results.pandas().xyxy[0])
        # print(coordinates)
        # print(coordinates[0])

        if ret==False:
            pass
        else:
            jpeg = cv2.imencode('.jpg', frame)[1]
            # send_message()
            # sendmail()
            # time.sleep(10)
            # frame,her = vid.read()
        # cv.imshow("hekk",frame)
            
	# /print(dummy_array)
            for i in dummy_array:
                if check(i,imgs,self.model) and self.flag:
                    print("&"*40)
                    print("accident")
                    send_message()
                    send_notification(1,True)
                    send_notification(2,False)
                    sendmail()
                    self.flag = False
            # update_data()
            return jpeg.tobytes()
    


    

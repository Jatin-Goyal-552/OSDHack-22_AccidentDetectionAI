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

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# from accidentdetectionapp.views import ref
# cred = credentials.Certificate('C:\\Users\\LENOVO\\projects\\Dot_Slash_Road_Safety\\smartai-3ebad-firebase-adminsdk-iwaiw-b65157f46b.json')
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://smartai-3ebad-default-rtdb.firebaseio.com/',
#     'databaseAuthVariableOverride': None
# })

# def update_data():
#     ref = db.reference("/")
#     # chdred = ref.child("Books")
#     # insert_data = ref.child("Books")
#     ref.set({
#     	"notify":
#     	{
#     		"Notification": "Accident happened ",
#             "accepted":0
#     	}
#     })


def send_notification():
    pusher_client = pusher.Pusher(
    app_id='1328110',
    key='4da6311b184ace45d1dc',
    secret='469709e6b17fadfab16f',
    cluster='ap2',
    ssl=True
    )
    notif = Notifications(notification="accident happened",lattitude=5756,longitude=455,accepted=0)
    notif.save()
    # article.title = 'This is the title'
    # article.contents = 'This is the content'
    # article.save()
    pusher_client.trigger('my-channel', 'my-event', {'message': 'Urgent\n please send ambulance as soon as possible at xyz address.'})
    return

def send_message():
    client = vonage.Client(key="4627a3c9", secret="KAd19Rz2sQ7HM3Tc")
    sms = vonage.Sms(client)
    responseData = sms.send_message(
        {
            "from": "Jatin Goyal",
            "to": "918168991401",
            "text": "Urgent \n Accident happened at raj labadi. Please send ambulance as soon as possible.",
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")

def sendmail():
    email_subject = "Urgent please send ambulance."
    email_body = "Accident happened at raj labadi please send ambulance as soon as possible"
    email="sachinkhandelwal9413@gmail.com"
    print(send_mail(email_subject, email_body,
                  settings.EMAIL_HOST_USER, [email], fail_silently=False))
    return 

class streaming(object):

    def __init__(self):
        print("hello")
        # self.video_capture = cv2.VideoCapture(0)
        self.video_capture = cv2.VideoCapture("C:\\Users\\LENOVO\\Downloads\\accident3.mp4")
        # self.model=torch.hub.load('ultralytics/yolov5', 'custom', path='C:\\Users\\LENOVO\\projects\\Dot_Slash_Road_Safety\\AccidentDetection\\best (2).pt',device='cpu')

    def get_frame(self):
        ret, frame = self.video_capture.read()
        # cv2.imwrite("image.jpg",frame)
        # imgs = cv2.imread("image.jpg")

        # results = self.model(imgs)
        
        # # if results.print()!="None":
        # #     print("*"*80)
        # #     # print(results.print())
        # #     print("*"*80)
        # print("*"*80)
        # print(results.pandas().xyxy[0].sort_values('xmin'))
        # print("*"*80)
        # # frame=cv2.imread(results.pandas().xyxy[0])
        if ret==False:
            pass
        else:
            jpeg = cv2.imencode('.jpg', frame)[1]
            # send_message()
            # sendmail()
            time.sleep(10)
            send_notification()
            # update_data()
            return jpeg.tobytes()
    


    
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.shortcuts import render, HttpResponse
from django.http.response import StreamingHttpResponse
from accidentdetectionapp.stream import streaming
from googleplaces import GooglePlaces, types, lang
import requests
import json
import vonage
import time
from .models import *
from django.shortcuts import redirect
import pusher
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# cred = credentials.Certificate('C:\\Users\\LENOVO\\projects\\Dot_Slash_Road_Safety\\smartai-3ebad-firebase-adminsdk-iwaiw-b65157f46b.json')
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://smartai-3ebad-default-rtdb.firebaseio.com/',
#     'databaseAuthVariableOverride': None
# })
# ref = db.reference("/")

# chdred = ref.child("Books")
# insert_data = ref.child()
# ref.set({
# 	"Books":
# 	{
# 		"Best_Sellers": -1
# 	}
# })

global hospital_name
hospital_name ="Unnamed"

def send_response():
    pusher_client = pusher.Pusher(
    app_id='1328110',
    key='4da6311b184ace45d1dc',
    secret='469709e6b17fadfab16f',
    cluster='ap2',
    ssl=True
    )
    # notif = Notifications(notification="accident happened",lattitude=5756,longitude=455,accepted=0)
    # notif.save()
    # article.title = 'This is the title'
    # article.contents = 'This is the content'
    # article.save()
    pusher_client.trigger('my-channel', 'my-event', {'message': 'Request Accepted'})
    return

def home(request):
    return render(request,'index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def webcam_feed(request):
    # print("W1")
    return StreamingHttpResponse(gen(streaming()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def maps(request):
    API_KEY = 'AIzaSyBj-F7jxbhMYXYn8WuLwZpnEInBX6S4Dew'
    google_places = GooglePlaces(API_KEY)

# call the function nearby search with
# the parameters as longitude, latitude,
# radius and type of place which needs to be searched of
# type can be HOSPITAL, CAFE, BAR, CASINO, etc
    query_result = google_places.nearby_search(
            # lat_lng ={'lat': 46.1667, 'lng': -1.15},
            lat_lng ={'lat': 28.4089, 'lng': 77.3178},
            radius = 5000,
            # types =[types.TYPE_HOSPITAL] or
            # [types.TYPE_CAFE] or [type.TYPE_BAR]
            # or [type.TYPE_CASINO])
            types =[types.TYPE_HOSPITAL])

    # If any attributions related
    # with search results print them
    if query_result.has_attributions:
        print (query_result.html_attributions)


    # Iterate over the search results
    for place in query_result.places:
        # print(type(place))
        # place.get_details()
        print (place.name)
        print("Latitude", place.geo_location['lat'])
        print("Longitude", place.geo_location['lng'])
        print()
    return render(request,'index.html')

# def send_mail(request):
#     client = vonage.Client(key="4627a3c9", secret="KAd19Rz2sQ7HM3Tc")
#     sms = vonage.Sms(client)
    
def hospital(request):
    return render(request,'hospital.html')

def test(request):
    global hospital_name
    notifications = Notifications.objects.all().order_by('-n_id') 
    # text = ref.child('notify').child('Notification').get()
    # accepted = ref.child('notify').child('accepted').get()
    # projectname = database.child('Data').child('Projectname').get().val()
    context = {
        'notifications': notifications,
        'hospital_name':hospital_name,
    }
    return render(request,"index2.html",context)

def accept(request,id):
    notification = Notifications.objects.filter(n_id=id).update(accepted = 1)
    send_response()
    return redirect('test')

def register(request):
    global hospital_name
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        latitude=request.POST.get('latitude')
        longitude=request.POST.get('longitude')
        print(name,email,latitude,longitude)
        hospital=Hospital(name=name,email=email,h_lattitude=latitude,h_longitude=longitude)
        hospital.save()
        hospital_name=name
        return redirect('test')
    return render(request, 'register.html')
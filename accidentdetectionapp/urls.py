from django.urls import path
from . import views


urlpatterns=[
    path('',views.home,name='home'),
    path("webcam_feed",views.webcam_feed,name='webcam_feed'),
    path("maps",views.maps,name='maps'),
    path("hospital",views.hospital,name='hospital'),
    path("test",views.test,name='test'),
    path("accept/<id>",views.accept,name='accept'),
    path("register",views.register,name='register'),
    # path("send_mail",views.send_mail,name='send_mail')
]
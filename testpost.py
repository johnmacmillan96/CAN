import json
from firebase import firebase
from canmsgs import *
from translation import *

##data = canIds.get('ID284')[0]
##firebase = firebase.FirebaseApplication('https://canbus-73c99.firebaseio.com', None)
##
##result = firebase.post('/test', data)

translateCAN('/home/pi/Documents/CAN/candump-2017-08-07_221543.log')

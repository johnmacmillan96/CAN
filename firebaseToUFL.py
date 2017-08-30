import json
import time
import requests
from requests.auth import HTTPBasicAuth
from firebase import firebase

# access the firebase
firebase = firebase.FirebaseApplication('https://canbus-73c99.firebaseio.com/', None)

# every 1/2 second, make a get request t the firebase, then put the data to the UFL connector
while True:
    json_data = firebase.get('/test/', 'dump')
    # make an empty string
    s = ''
    # fill the string with the json messages
    for point in json_data:
        s += point.get('property') +  ',' + str(point.get('time')) +  ',' + str(point.get('value')) + '\n'

    # put to UFL
    r = requests.put('https://my-ufl-connector:5450/connectordata/CANrest/',
                      auth = HTTPBasicAuth('passwordispi', 'pi'), data=s, verify=False)
    # wait 0.5 seconds
    time.sleep(0.5)

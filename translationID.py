import re
import os
import json
import datetime
from firebase import firebase
from canmsgs import *


class NoTranslationData(Exception):
    pass

def translateCAN(filename):

    # firebase
    fb = firebase.FirebaseApplication('https://canbus-73c99.firebaseio.com', None)

    # process the file
    processFileJSON(filename, fb)

def processFileJSON(filename, fb):
    # get lines from file
    file = open(filename, "r")
    lines = file.readlines()
    file.close()
    
    jsonList = []

    # process file while writing to jsonList
    for line in lines:
        processLineJSON(line, jsonList)

    post = fb.put('/test', 'dump', jsonList)


def processLineJSON(line, jsonList):
    # split line into seperate packets
    split = re.split("\W", line)

    time = split[1] + "." + split[2]   # time vale
    id = split[5]                    # ID
    data = split[6]                    # data

    ID = ('ID' + id)

    # checks if there is translation data, otherwise raises exception
    if (ID in canIds):
        ID = canIds.get(ID)
    else:
        raise NoTranslationData('There is no translation data for' + id)    

    for i in range(7):
        # the name of the data
        name = ID[i].get('name')
        # if the name is NA, there is no data and it is skipped
        if (name != 'NA'):
            # the byte
            byte = i + 1
            # the coefficient to translate into readable data
            coeff = ID[i].get('coeff')
            # if the current byte is a 'High' byte, uses the preceding byte as a 'Low' byte
            highlow = ID[i].get('highlow')

            # translate the data
            translatedD = translation(byte, coeff, highlow, data)

            # write the data to the new file
            json = {'time' : datetime.datetime.utcfromtimestamp(float(time)), 'property' : name, 'value' : translatedD}
            jsonList.append(json)

            # if the byte is a high byte, the preceding byte gets processed with it,
            # so it does not require a separate analysis and is skipped
            if (highlow):
                i = i + 1

def translation(byte, coeff, highlow, data):

    # gets the lower range
    rangeL = byte*2 - 2
    # gets the upper range
    if (highlow):
        rangeH = byte*2 + 2
    else:
        rangeH = byte*2

    # takes a substring of the specific byte needed
    # and multiplies by its coefficient
    data = int(data[rangeL:rangeH], 16) * coeff
    return data

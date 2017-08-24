import re
import os
import json
import datetime
from firebase import firebase
from canmsgs import *


class NoTranslationData(Exception):
    pass

# param filename
#   the file to process
def translateCAN(filename):

    # accesses the firebase
    fb = firebase.FirebaseApplication('https://canbus-73c99.firebaseio.com', None)

    # process the file
    processFileJSON(filename, fb)


# param filename
#   the file to process
# param fb
#   the firebase db to send the data to
def processFileJSON(filename, fb):
    # get lines from file
    file = open(filename, "r")
    lines = file.readlines()
    file.close()

    # create an empty list to fill with json objects
    jsonList = []

    # process file while writing to jsonList
    for line in lines:
        processLineJSON(line, jsonList)

    # uses a put command to send the list to the firebase db
    post = fb.put('/test', 'dump', jsonList)


# param line
#   the line of data to process. consists of a time, id, and data
# param jsonList
#
def processLineJSON(line, jsonList):
    # split line into seperate string
    split = re.split("\W", line)

    time = split[1] + "." + split[2]    # time vale
    id = split[5]                       # ID
    data = split[6]                     # data

    # adds the string for dict look-up
    ID = ('ID' + id)

    # checks if there is translation data, otherwise raises exception
    if (ID in canIds):
        ID = canIds.get(ID)
    else:
        raise NoTranslationData('There is no translation data for' + id)    

    # loops through each byte of data
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

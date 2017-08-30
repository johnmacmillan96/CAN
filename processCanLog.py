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
    # replace this with your firebase url
    fb = firebase.FirebaseApplication('https://your-firebase-url.firebaseio.com', None)

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
#   the list of json messages to put onto the firbase db
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
            bitLength = ID[i].get('bitLength')

            # translate the data
            translatedD = translation(byte, coeff, bitLength, data)

            # write the data to the new file
            json = {'time' : datetime.datetime.utcfromtimestamp(float(time)), 'property' : name, 'value' : translatedD}
            jsonList.append(json)

            # if the byte is a high byte, the preceding byte gets processed with it,
            # so it does not require a separate analysis and is skipped
            if (bitLength > 8):
                i = i + 1

# param byte
#   the byte being translated
# param coeff
#   the coefficient to multiply the decimal value by to get meaningful data
# param bitLength
#   the ammount of bits that store meaningful data
# param data
#   the data to translate
def translation(byte, coeff, bitLength, data):

    # gets the lower range
    rangeL = byte*2 - 2
    # gets the upper range
    if (bitLength > 8):
        rangeH = byte*2 + 2
    else:
        rangeH = byte*2

    # takes the first byte, converts it from hexadecimal to integer,
    # then does a bit shift by the bitLength - 8. does the same to the
    # second byte, but with a bit shift of 16 minus the bitLength. then
    # adds them together, and multiplys by the coefficient
    val = ((int(data[rangeL:rangeL + 2], 16) << (bitLength - 8)) +
           (int(data[rangeL + 2:rangeH], 16) >> (16 - bitLength))) * coeff

    return val

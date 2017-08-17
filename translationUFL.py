# this script translates hexidecimal CAN messages into to decimal
import re
import os
import json
import requests
from canmsgs import *

class NoTranslationData(Exception):
    pass

def translateCAN(filename):
    # access the correct id from canIds dict
    id = ('ID' + getID(filename))

    # checks if there is translation data, otherwise raises exception
    if (id in canIds):
        id = canIds.get(id)
    else:
        raise NoTranslationData('There is no translation data for' + id)
    
    # loops through each byte, first checking if there is any data on the byte,
    # if there is it processes it and saves it as a new file

    rest = 'https://PISRV01:5460/connectordata/REST endpoint/'
    
    for i in range(7):
        # the name of the data
        name = id[i].get('name')
        # if the name is NA, there is no data and it is skipped
        if (name != 'NA'):
            # the byte
            byte = i + 1
            # the coefficient to translate into readable data
            coeff = id[i].get('coeff')
            # if the current byte is a 'High' byte, uses the preceding byte as a 'Low' byte
            highlow = id[i].get('highlow')

            # processes the file for the data
            processFile(filename, name, byte, coeff, highlow, rest)
            #processFile(filename, name, byte, coeff, highlow)
            


            # if the byte is a high byte, the preceding byte gets processed with it,
            # so it does not require a separate analysis and is skipped
            if (highlow):
                i = i + 1


def getID(filename):
    file = open(filename, "r")
    line = file.readline()
    file.close()

    split = re.split("\W", line)
    return split[5]


def processFile(filename, name, byte, coeff, highlow, rest):
        # get lines from file
        file = open(filename, "r")
        lines = file.readlines()
        file.close()

        # create new filename
        filename = filename[-3] + name + 'TRANSLATED.txt'
        newFile = open(filename, "w")

        # process old file saving into new file
        for line in lines:
            processLine(byte, coeff, highlow, line, newFile)

        newFile.close()

        headers = {'UserName' : 'passwordispi', 'Password' : 'pi'}
        files = {'file' : open(filename, 'rb')} 
        r = requests.post(rest, files=files, headers=headers)



def processLine(byte, coeff, highlow, line, newFile):
    # split line into seperate packets
    split = re.split("\W", line)

    t = split[1] + "." + split[2]   # time vale
    i = split[5]                    # ID
    d = split[6]                    # data

    # translate the data
    translatedD = translation(byte, coeff, highlow, d)

    # write the data to the new file
    newFile.write(t + " ")
    newFile.write(i + " ")
    newFile.write(str(translatedD) + "\n")


##def processFileJSON(filename, name, byte, coeff, highlow, fb):
##    # get lines from file
##    file = open(filename, "r")
##    lines = file.readlines()
##    file.close()
##    
##    jsonList = []
##
##    # process old file saving into new file
##    for line in lines:
##        processLineJSON(byte, coeff, highlow, line, jsonList)
##
##    post = fb.post('/test', {'data' : jsonList})   
##
##
##def processLineJSON(byte, coeff, highlow, line, jsonList):
##    # split line into seperate packets
##    split = re.split("\W", line)
##
##    t = split[1] + "." + split[2]   # time vale
##    i = split[5]                    # ID
##    d = split[6]                    # data
##
##    # translate the data
##    translatedD = translation(byte, coeff, highlow, d)
##
##    # write the data to the new file
##    json = {'time' : t, 'ID' : i, 'data' : str(translatedD)}
##    jsonList.append(json)

# param data: the hex data to translate
# param byte: the specific byte in the data
# param highlow: true/false if there is a high and low byte
# param coeff: the coefficient to translate the decimal
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














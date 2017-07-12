import serial
import time
import cv2
import numpy as np
from grip import GripPipeline


"""GLOBALS"""
global xdist
xdist= 0
global ydist
ydist= 0
"""SERIAL PORTS"""
ser = serial.Serial()
ser.port = "COM4"
ser.baudrate = 9600
ser.stopbits = 1
ser.parity = "N"
ser.bytesize = 8
ser.open()
#
"""VISION CODE"""


def getXY():
    cap = cv2.VideoCapture(0)
    pipeline = GripPipeline()
    have_frame, frame = cap.read()
    print(frame.shape)
    if have_frame:
        pipeline.process(frame)
        center_x_positions = []
        center_y_positions = []
        widths = []
        heights = []
        # Find the bounding boxes of the contours to get x, y, width, and height
        for contour in pipeline.filter_contours_output:
            x, y, w, h = cv2.boundingRect(contour)
            center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
            center_y_positions.append(y + h / 2)
            widths.append(w)
            heights.append(h)
            print(center_x_positions[0])
            print(center_y_positions[0])
            return center_x_positions[0], center_y_positions[0]


"""TRANSLATIONS"""

def generateStatement():
    xgen , ygen = getXY()
    xgen = (480-xgen)*(.67)
    ygen = (320-ygen)*(.7)
    xgen = int(round(xgen))
    ygen= int(round(ygen))
    expression = "DW -" + str(xgen) + "," + str(ygen) + ",0\n"
    print("expression is:", expression, "encoded expression is:", expression.encode())
    var = expression.encode()
    return var

"""ARM CODE"""

# Positions
# Origin: +96.5,+236.5,+72.1,-89.0,+180.0
# PLACE +88.8,+378.2,+122.0,-88.9,+153.9
# Camera: -58.1,+306.1,+111.9,-88.8,+160.7

# ser.write(b'MP -58.2,+306.2,+112.0,-88.9,+153.9\n')
# time.sleep(6)
# ser.write(b'gc\n')
# time.sleep(2)
#
#
def GrabAllCubes():
    height = 55
    ser.write(b'SP 8\n')
    ser.write(b'MP -58.1,+306.1,+111.9,-88.8,+160.7\n')
    time.sleep(2)
    ser.write(b'GC\n')
    while(getXY()!=0):
        print("Iteration")
        var = generateStatement()
        time.sleep(1)
        ser.write(b'MP +96.5,+236.5,+72.1,-89.0,+180.0\n')
        time.sleep(2)
        ser.write(b'go\n')
        time.sleep(1)
        ser.write(var)
        time.sleep(2)
        expression = "DW 0,0,-55\n"
        expression = expression.encode()
        ser.write(expression)
        time.sleep(2)
        ser.write(b'GC\n')
        time.sleep(1)
        expression = "DW 0,0," + str(height) + "\n"
        expression = expression.encode()
        ser.write(expression)
        time.sleep(2)
        ser.write(b'MP +62.8,+383.2,+117.0,-88.9,+153.9\n')
        time.sleep(2)
        expression = "DW 0,0,-" + str(160-height) + "\n"
        expression = expression.encode()
        ser.write(expression)
        time.sleep(2)
        ser.write(b'GO\n')
        time.sleep(2)
        ser.write(b'DW 0,0,40\n')
        time.sleep(2)
        ser.write(b'MP -58.1,+306.1,+111.9,-88.8,+160.7\n')
        time.sleep(2)
        ser.write(b'GC\n')
        height = height+20
        # if(height == 155):
        #     break



GrabAllCubes()
#
# ser.write(b'MJ 0,0,0,0,1\n')

# time.sleep(3)
# var = generateStatement()
# ser.write(b'MP +96.5,+236.5,+72.1,-89.0,+180.0\n')
# time.sleep(5)
# ser.write(b'go\n')
# time.sleep(2)
# ser.write(var)
# time.sleep(6)
# ser.write(b'DW 0,0,-55\n')
# time.sleep(2)
# ser.write(b'gc\n')
# time.sleep(1)
# ser.write(b'DW 0,0,tera20\n')
# time.sleep(2)
# ser.write(b'MP +88.8,+378.2,+122.0,-88.9,+153.9\n')
# time.sleep(6)
# ser.write(b'DW 0,0,-95\n')
# time.sleep(7)
# ser.write(b'GO\n')
# time.sleep(2)
# ser.write(b'DW 0,0,90\n')
# time.sleep(5)
# ser.write(b'MP -58.2,+306.2,+112.0,-88.9,+153.9\n')
# time.sleep(5)
# ser.write(b'GC\n')
#
#
# time.sleep(3)
# var = generateStatement()
# ser.write(b'MP +96.5,+236.5,+72.1,-89.0,+180.0\n')
# time.sleep(5)
# ser.write(b'go\n')
# time.sleep(2)
# ser.write(var)
# time.sleep(6)
# ser.write(b'DW 0,0,-55\n')
# time.sleep(2)
# ser.write(b'gc\n')
# time.sleep(1)
# ser.write(b'DW 0,0,55\n')
# time.sleep(2)
# ser.write(b'MP +88.8,+378.2,+122.0,-88.9,+153.9\n')
# time.sleep(6)
# ser.write(b'DW 0,0,-75\n')
# time.sleep(7)
# ser.write(b'GO\n')
# time.sleep(2)
# ser.write(b'DW 0,0,90\n')
# time.sleep(5)
# ser.write(b'MP -58.2,+306.2,+112.0,-88.9,+153.9\n')
# time.sleep(5)
# ser.write(b'GC\n')


# ser.write(b'NT\n')



# ser.write(b'RS\n')











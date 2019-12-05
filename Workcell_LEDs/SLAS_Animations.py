# -*- coding: utf-8 -*-
"""
Animations for SLAS trade show.
Animation array now in form [R, G, B, Brightness].
Program will now initialise LEDs to be at full brightness and then scale down colours to allow for change in brightness

Author:    Sean Woodward
Date:      01/11/2019
"""

#Import relevant libraries
import time
import math
import colorsys
import queue
import logging
import numpy as np

#Default for queues
q = queue.Queue()

#Function to check wait queue
def ThreadCheck(q, runLoop):
    #logging.debug("checking queue")
    if q.empty() == False:
        logging.debug("exiting animation - runLoop set to False")
        x = q.get()
        runLoop = False
        return runLoop
    else:
        return runLoop

"""Functions to control LEDs"""
#Non-normalised HSV to RGB function
def HsvToRgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

#Run complete - Run rainbow animation
def RunComplete(strip, q, waitTime=10):
    runLoop = True
    ledCount = len(strip)
    while runLoop == True:
        for i in range(ledCount):
            for j in range(ledCount):
                runLoop = ThreadCheck(q, runLoop)
                if runLoop == False: break
                strip[j] = HsvToRgb((((j+i)%ledCount)/ledCount),1.0,1.0)
            if runLoop == False: break
            strip.show()
    logging.debug("exiting RunComplete animation - runLoop loop exited")

#TeachMode - Pulsing yellow
def TeachMode(strip, q, waitTime=10):
    runLoop = True
    ledCount = len(strip)
    array = np.zeros((ledCount,4))
    strip.fill((255,255,0))
    strip.show()
    while runLoop==True:
        for i in [1,0.9,0.8,0.7,0.6,0.5,0.6,0.7,0.8,0.9,1]:
            for j in range(ledCount):
                runLoop = ThreadCheck(q, runLoop)
                if runLoop == False: break
                strip[j,0] = int(strip[j,0] * i)
                strip[j,1] = int(strip[j,1] * i)
                strip[j,2] = int(strip[j,2] * i)
            if runLoop == False: break
            strip.show()            
    logging.debug("exiting TechMode animation - runLoop loop exited")

#Main program logic
if __name__ == '__main__':
    print("This program contains animations for use at SLAS")
    x = np.zeros((2,4))
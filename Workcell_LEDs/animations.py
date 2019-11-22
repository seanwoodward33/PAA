# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Program to control LEDs from Raspberry Pi

Author:	Sean Woodward
Date:		01/11/2019

For further information on AdaFruits NeoPixel Library, see: https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
Inspirtaion drawn from tutorial, see: https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/
"""

#Import relevant libraries
import time
import math
import colorsys
import queue
import logging

#Default for queues
q=queue.Queue()

#Function to check wait loop
def ThreadCheck(q, runLoop):
    if q.empty == False:
        logging.debug("exiting animation")
        x = q.get()
        runLoop = False
        return runLoop
    else:
        return runLoop

#Define functions to control LEDs
#Wipe colour across pixel line, one pixel at a time
def ColourWipe(strip, colour, backColour = (0,0,0), waitTime=10, q=q):                     #waitTime is in ms
    logging.debug
    runLoop = True
    while runLoop == True:
        for i in range(len(strip)):
            runLoop = ThreadCheck(q, runLoop)
            strip[i] = colour
            strip.show()
            time.sleep(waitTime/1000.0)
        strip.fill(backColour)
        strip.show()

#Wipe colour across pixel line, one pixel at a time from each end
def ColourWipeTwo(strip, colour, backColour = (0,0,0), waitTime=20, q=q):                  #waitTime is in ms
    runLoop = True
    while runLoop == True:
        for i in range(math.ceil(len(strip)/2)):
            runLoop = ThreadCheck(q, runLoop)
            strip[i] = colour
            strip[len(strip)-1-i] = colour
            strip.show()
            time.sleep(waitTime/1000.0)
        strip.fill(backColour)
        strip.show()

#Single pixel progression
def SinglePixelWipe(strip, singleColour, backColour = (0,0,0), waitTime=10, q=q):
    runLoop = True
    while runLoop == True:
        strip.fill(backColour)
        for i in range(len(strip)):
            if (i > 0):
                runLoop = ThreadCheck(q, runLoop)
                strip[i-1] = backColour
                strip[i] = singleColour
                strip.show()
                time.sleep(waitTime/1000.0)

#Single pixel progression with retention
def SinglePixelWipeRetain(strip, singleColour, backColour = (0,0,0), waitTime=0, q=q):
    runLoop = True
    while runLoop == True:
        strip.fill(backColour)
        for i in range(len(strip)):
            for j in range(len(strip)-i):
                if (j > 0):
                    runLoop = ThreadCheck(q, runLoop)
                    strip[j-1] = backColour
                    strip[j] = singleColour
                    strip.show()
                    time.sleep(waitTime/1000.0)

#Pixel progression
def PixelWipe(strip, singleColour, wipeLength = 4, backColour = (0,0,0), waitTime=10, q=q):
    runLoop = True
    while runLoop == True:
        strip.fill(backColour)
        for i in range(len(strip) + wipeLength):
            for j in range(wipeLength):
                if (i-j > 0 and i-j < len(strip)):
                    runLoop = ThreadCheck(q, runLoop)
                    strip[i-j] = singleColour
                    strip[i-wipeLength] = backColour
                    strip.show()
                    time.sleep(waitTime/1000.0)


#Pixel progression with retention
def PixelWipeRetain(strip, singleColour, wipeLength = 4, backColour = (0,0,0), waitTime=0, q=q):
    runLoop = True
    while runLoop == True:
        strip.fill(backColour)
        for i in range(len(strip)+wipeLength):
            for j in range(len(strip)-(i*wipeLength)):
                for k in range(wipeLength):
                    if (j-k > 0 and j-k < len(strip)-i):
                        runLoop = ThreadCheck(q, runLoop)
                        strip[j-k] = singleColour
                        strip[j-wipeLength] = backColour
                        strip.show()
                        time.sleep(waitTime/1000.0)


#Movie theatre light style chaser animation
def TheatreChase(strip, colour, waitTime=50, q=q):    #waitTime is in ms
    runLoop = True
    while runLoop == True:
        for j in range(3):
            for k in range(0,len(strip),3):
                if(k+j < len(strip)):
                    runLoop = ThreadCheck(q, runLoop)
                    strip[k+j] = colour
            strip.show()
            time.sleep(waitTime/1000.0)
            for k in range(0,len(strip),3):
                if(k+j < len(strip)):
                    runLoop = ThreadCheck(q, runLoop)
                    strip[k+j] = 0
            strip.show()

#Non-normalised HSV to RGB function
def HsvToRgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

#Draw a rainbow that fades across all the LEDs at once
def Rainbow(strip, waitTime=10, q=q):
    runLoop = True
    ledCount = len(strip)
    while runLoop == True:
        for i in range(ledCount):
            for j in range(ledCount):
                runLoop = ThreadCheck(q, runLoop)
                strip[j] = HsvToRgb((((j+i)%ledCount)/ledCount),1.0,1.0)
            strip.show()

#Knightrider
def Knightrider(strip, waitTime, q=q):
    runLoop = True
    ledCount = len(strip)
    direction = "up"
    while runLoop == True:
        for i in range(iterations):
            if (direction == "up"):
                pass
        pass

#Set solid colour
def SolidColour (strip, colour, q=q):
    runLoop = True
    while runLoop == True:
        runLoop = ThreadCheck(q, runLoop)
        strip.fill(colour)
        strip.show()

#Main program logic
if __name__ == '__main__':
    print("This program contains animations for use in the LED Pi Controller")
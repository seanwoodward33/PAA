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

#Define functions to control LEDs
#Wipe colour across pixel line, one pixel at a time
def ColourWipe(strip, colour, waitTime=10):                     #waitTime is in ms
    for i in range(len(strip)):
        strip[i] = colour
        strip.show()
        time.sleep(waitTime/1000.0)

#Wipe colour across pixel line, one pixel at a time
def ColourWipeTwo(strip, colour, waitTime=20):                  #waitTime is in ms
    for i in range(math.ceil(len(strip)/2)):
        strip[i] = colour
        strip[len(strip)-1-i] = colour
        strip.show()
        time.sleep(waitTime/1000.0)

#Single pixel progression
def SinglePixelWipe(strip, singleColour, backColour = (0,0,0), waitTime=10):
    strip.fill(backColour)
    for i in range(len(strip)):
        if (i > 0):
            strip[i-1] = backColour
        strip[i] = singleColour
        strip.show()
        time.sleep(waitTime/1000.0)

#Single pixel progression with retention
def SinglePixelWipeRetain(strip, singleColour, backColour = (0,0,0), waitTime=0):
    strip.fill(backColour)
    for i in range(len(strip)):
        for j in range(len(strip)-i):
            if (j > 0):
                strip[j-1] = backColour
            strip[j] = singleColour
            strip.show()
            time.sleep(waitTime/1000.0)

#Pixel progression
def PixelWipe(strip, singleColour, wipeLength = 4, backColour = (0,0,0), waitTime=10):
    strip.fill(backColour)
    for i in range(len(strip) + wipeLength):
        for j in range(wipeLength):
            if (i-j > 0 and i-j < len(strip)):
                strip[i-j] = singleColour
        strip[i-wipeLength] = backColour
        strip.show()
        time.sleep(waitTime/1000.0)


#Pixel progression with retention
def PixelWipeRetain(strip, singleColour, wipeLength = 4, backColour = (0,0,0), waitTime=0):
    strip.fill(backColour)
    for i in range(len(strip)):
        for j in range(len(strip)-i):
            if (j > 0):
                strip[j-1] = backColour
            strip[j] = singleColour
            strip.show()
            time.sleep(waitTime/1000.0)


#Movie theatre light style chaser animation
def TheatreChase(strip, colour, waitTime=50, iterations=30):    #waitTime is in ms
    for i in range(iterations):
        for j in range(3):
            for k in range(0,len(strip),3):
                if(k+j < len(strip)):
                    strip[k+j] = colour
            strip.show()
            time.sleep(waitTime/1000.0)
            for k in range(0,len(strip),3):
                if(k+j < len(strip)):
                    strip[k+j] = 0
            strip.show()

#Non-normalised HSV to RGB function
def HsvToRgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

#Draw a rainbow that fades across all the LEDs at once
def Rainbow(strip, waitTime=10, iterations = 500):
    ledCount = len(strip)
    for i in range(iterations):
        for j in range(ledCount):
            strip[j] = HsvToRgb((((j+i)%ledCount)/ledCount),1.0,1.0)
        strip.show()

#Knightrider
def Knightrider(strip, waitTime, iterations = 500):
    ledCount = len(strip)
    direction = up
    for i in range(iterations):
        if (direction == up):
            pass
    pass


#Emergency Stop, Red lights
def ErrorState(strip):
    strip.fill((255,0,0))
    strip.show()

#Emergency Stop, Red lights
def RunState(strip):
    strip.fill((0,255,0))
    strip.show()

#Set solid colour
def SolidColour (strip, colour):
    strip.fill(colour)
    strip.show()

#Main program logic
if __name__ == '__main__':
    print("This program contains animations for use in the LED Pi Controller")
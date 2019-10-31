#!/usr/bin/env python3
#
#Program to control LEDs from Raspberry Pi
#
#Author:	Sean Woodward
#Date:		30/10/2019
#
#For further information on AdaFruits NeoPixel Library, see: https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
#Inspirtaion drawn from tutorial, see: https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/

#Import relevant libraries
import time
import neopixel
import board
import math
import threading


#Define LED strip configuration
def LedSetup(ledPin = board.D18, ledCount = 25, ledOrder = neopixel.GRB):
    ledPin = board.D18						                        #GPIO pin LEDs are connected to Pi
    ledCount = 49							                        #Number of LEDs in strip
    ledOrder = neopixel.GRB                                         #Set to *.GRB or *.RGB depending on how LEDs are wired
    ledStrip = neopixel.NeoPixel(ledPin, ledCount, brightness=0.2, auto_write=False, pixel_order=ledOrder)
    return ledStrip

#Define functions to control LEDs
def ColourWipe(strip, colour, waitTime=50):                     #waitTime is in ms
    #Wipe colour across pixel line, one pixel at a time
    for i in range(len(strip)):
        strip[i] = colour
        strip.show()
        time.sleep(waitTime/1000.0)

def ColourWipeTwo(strip, colour, waitTime=50):                  #waitTime is in ms
	#Wipe colour across pixel line, one pixel at a time
    for i in range(math.ceil(len(strip)/2)):
        strip[i] = colour
        strip[len(strip)-1-i] = colour
        strip.show()
        time.sleep(waitTime/1000.0)

def TheatreChase(strip, colour, waitTime=50, iterations=10):    #waitTime is in ms
    #Movie theatre light style chaser animation
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

def ErrorState(strip):
    strip[:] = = (0,255,0)
    #for i in range(len(strip)):
    #    strip[i] = (0,255,0)
    strip.show()

#Main program logic
if __name__ == '__main__':
    #Initialise LED strip
    ledStrip = LedSetup()
    
    #Testing Loop
    try:
        while True:
            ColourWipe(ledStrip, (255,0,0), 0)
            ColourWipe(ledStrip, (0,255,0), 0)
            ColourWipe(ledStrip, (0,0,255), 0)
            ColourWipeTwo(ledStrip, (0,255,0), 50)
            TheatreChase(ledStrip, (255,255,255))
            ErrorState(ledStrip)
            
    except KeyboardInterrupt:
        ColourWipe(ledStrip, (0,0,0), 10)

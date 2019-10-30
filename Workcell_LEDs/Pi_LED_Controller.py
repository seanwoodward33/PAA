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


#Define LED strip configuration
ledPin = board.D18						#GPIO pin LEDs are connected to Pi
ledCount = 25							#Number of LEDs in strip
ledOrder = neopixel.GRB						#Set to *.GRB or *.RGB depending on how LEDs are wired
ledStrip = neopixel.NeoPixel(ledPin, ledCount, brightness=0.2, auto_write=False, pixel_order=ledOrder)

#Define functions to control LEDs
def colourWipe(strip, colour, waitTime=50):
	#Wipe colour across pixel line, one pixel at a time
	for i in range(strip.numPixels()):
		strip.setPixelColour(i, colour)
		strip.show()
		time.sleep(waitTime/1000.0)

def colourWipeTwo(strip, colour, waitTime=50):
	#Wipe colour across pixel line, one pixel at a time
	for i in range(math.ceil(strip.numPixels()/2)):
		strip.setPixelColour(i, colour)
		strip.setPixelColour(strip.numPixels()-i, colour)
		strip.show()
		time.sleep(waitTime/1000.0)

def theatreChase(strip, colour, waitTime=50, iterations=10):
    #Movie theatre light style chaser animation
    for i in range(iterations):
        for j in range(3):
            for k in range(0,strip.numPixels(),3):
                strip.setPixelColour(k+j, colour)
            strip.show()
            time.sleep(waitTime/1000.0)
            for k in range(0,strip.numPixels(),3):
                strip.setPixelColour(k+j, 0)


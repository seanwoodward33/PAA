# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
#Program to control LEDs from Raspberry Pi
#
#Author:	Sean Woodward
#Date:		30/10/2019
#
#For further information on AdaFruits NeoPixel Library, see: https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage
#Inspirtaion drawn from tutorial, see: https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/
"""

#Import relevant libraries
import neopixel
import board

#Import animations from separate file
import animations

#Define LED strip configuration
def LedSetup(ledPin = board.D18, ledCount = 25, ledOrder = neopixel.GRB):
    ledPin = board.D18						                        #GPIO pin LEDs are connected to Pi
    ledCount = 98							                        #Number of LEDs in strip
    ledOrder = neopixel.GRB                                         #Set to *.GRB or *.RGB depending on how LEDs are wired
    ledStrip = neopixel.NeoPixel(ledPin, ledCount, brightness=0.2, auto_write=False, pixel_order=ledOrder)
    return ledStrip

def LedShutdown():
    neopixel.NeoPixel.deinit()  
    
#Colour definitions
paaDarkBlue = (2,116,153)
paaLightBlue = (53,177,203)
paaSlabPri = (201,208,34)
paaSlabSec = (77,138,45)
paaScelPri = (230,81,151)
paaScelSec = (151,19,75)
paaKx2Pri = (247,175,00)
paaKx2Sec = (239,121,38)
paaSrunPri = (81,40,125)
paaSrunSec = (60,23,92)
paaStorPri = (00,144,208)
paaStorSec = (00, 89, 163)


#Main program logic
if __name__ == '__main__':
    #Initialise LED strip
    ledStrip = LedSetup()
    
    #Testing Loop
    try:
        while True:
            #animations.ColourWipe(ledStrip, (255,0,0), 0)
            #animations.ColourWipe(ledStrip, (0,255,0), 0)
            #animations.ColourWipe(ledStrip, (0,0,255), 0)
            #animations.ColourWipeTwo(ledStrip, (0,255,0))
            #animations.SinglePixelWipe(ledStrip,(255,0,255))
            animations.Rainbow(ledStrip, 1, 2000)
            #animations.PixelWipe(ledStrip,(255,0,255))
            #animations.PixelWipeRetain(ledStrip,(255,0,255))
            #animations.SinglePixelWipeRetain(ledStrip,(255,0,255))
            
    except KeyboardInterrupt:
        animations.ColourWipe(ledStrip, (0,0,0), int(1000/len(ledStrip)))

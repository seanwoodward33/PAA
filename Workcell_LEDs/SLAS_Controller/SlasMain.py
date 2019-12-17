    # -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:39:07 2019

@author: Sean_Woodward

Main.py - Program to run to control whole system
"""

#Import libraries
import threading
import queue
import time
import logging
import board
import neopixel
import numpy as np
import datetime
import random
import colorsys
import pulseio
import RPi.GPIO as GPIO


#Import other code
import SlasAnimations

#Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(asctime)s - (%(threadName)-10s) %(message)s')

#Setup GPIO mode
GPIO.setmode(GPIO.BOARD)

#Define workcell class
class Workcell():
    def __init__(self):
        self.animationRun = True
        self.firstRun = True
        self.pulseDirection = "Down"
        self.dimLevelLeds = 0.3
        self.runTime = datetime.datetime.now()
        self.runFinishTime = datetime.datetime.now()
        self.percentageComplete = 0.0
        self.runLength= datetime.timedelta(seconds = 7)
        self.endRunTime = datetime.datetime.now()
        self.endRunFinishTime = datetime.datetime.now()
        self.endRunPercentage = 0.0
        self.endRunLength= datetime.timedelta(seconds = 3)
        self.estops = [True, False, False]
        self.estopPositions = [[0,5],[46,56],[293,302]]
        self.doors = [False, False, False, False, False, False]
        self.doorPositions = [[6,45],[55,100],[117,232],[117,232],[248,292],[303,344]]
    
    def LedSetup(self, ledGpioPin, ledCount, ledBrightness, ledOrder = neopixel.GRB):
        self.ledPin = ledGpioPin
        self.ledCount = ledCount
        self.ledBrightness = ledBrightness
        self.ledOrder = ledOrder
        self.ledArray = np.zeros((ledCount,4))
        self.ledArray[:,3] = self.ledBrightness

    
    def LedInitialise(self):
        self.ledStrip = neopixel.NeoPixel(self.ledPin, self.ledCount, brightness = self.ledBrightness, pixel_order=self.ledOrder, auto_write=False)
    
    def LedSections(self, sections = [[0,98]]):
        self.ledSections = sections
        self.firstRun = [True]*len(self.ledSections)
    
    def LedSectionAnimations(self, animations = ["RunComplete"]): #default runcomplete rainbow used
        self.ledSectionAnimations = animations
    
    def AnimationCall(self, input, section):
            method = getattr(self,input)
            return method(section)
    
    def UpdateBySection(self):
        for i in range(len(self.ledSections)):
            self.AnimationCall(self.ledSectionAnimations[i], i)
    
    def OutputLeds(self):
        for i in range(self.ledCount):
            #print (str(i) + " " + str(self.ledArray[i]))
            x = np.rint(self.ledArray[i][0:3]*self.ledArray[i,3]).astype(int)
            self.ledStrip[i] = (x[0],x[1],x[2])
        self.ledStrip.show()        
    
    def RunComplete(self, i):
        SlasAnimations.RunComplete(self, i)
    
    def TeachMode(self, i):
        SlasAnimations.TeachMode(self, i)

    def DoorOpen(self, i):
        SlasAnimations.DoorOpen(self, i)
    
    def SystemRunningShort(self, i):
        SlasAnimations.SystemRunningShort(self, i)
    
    def SystemRunningLong(self, i):
        SlasAnimations.SystemRunningLong(self, i)
    
    def EStop(self,i):
        SlasAnimations.EStop(self,i)

#Setup pins for RGB filter LEDs
redPin = GPIO.PWM(11, 1000)
greenPin = GPIO.PWM(12, 1000)
bluePin = GPIO.PWM(13, 1000)

rgbPwmValues = (0,0,0)

redPin.start(rgbPwmValues[0])
greenPin.start(rgbPwmValues[1])
bluePin.start(rgbPwmValues[2])

"""
redPin = pulseio.PWMOut(board.D11, frequency=5000, duty_cycle=0)
greenPin = pulseio.PWMOut(board.D12, frequency=5000, duty_cycle=0)
bluePin = pulseio.PWMOut(board.D13, frequency=5000, duty_cycle=0)
"""

def RgbCycle(i):
    i = colorsys.rgb_to_hsv(i)
    i = colorsys.hsv_to_rgb((i[0]+0.01)%1, 1, 1)
    return i


if __name__ == '__main__':
    logging.debug("Main SLAS control program running")
    
    logging.debug("Create SLAS workcell object")
    SLAS = Workcell()
    
    logging.debug("Create SLAS LED strip")
    SLAS.LedSetup(board.D18, 348, 1)
    
    logging.debug("Initialise LEDs")
    SLAS.LedInitialise()
    
    logging.debug("Setting up LED sections")
    SLAS.LedSections([[0,110],[111,238],[239,348]]) #Section 1 - [0,110], section 2 - [111,238], section 3 =- [239,348]
    
    #Create list of all programmed animations to cycle through
    animationsTaught = ["RunComplete", "TeachMode", "EStop", "DoorOpen", "SystemRunningShort", "EStop", "SystemRunningLong"]
    logging.debug("Setting animation to be first two animations in animationsTaught list")
    SLAS.LedSectionAnimations([animationsTaught[0], animationsTaught[1],animationsTaught[2]])
    
    
    logging.debug("Updating for all sections, forever loop times")
    x = 0
    while x < 1000:
        SLAS.UpdateBySection()
        SLAS.OutputLeds()
        x = x + 1
        
        redPin.ChangeDutyCycle(rgbPwmValues[0]*100)
        greenPin.ChangeDutyCycle(rgbPwmValues[1]*100)
        bluePin.ChangeDutyCycle(rgbPwmValues[2]*100)
        
        rgbPwmValues = RgbCycle(rgbPwmValues)
        
        if x == 950:
            x = 0
            animationsTaught = animationsTaught[1:] + animationsTaught[:1]
            for i in range(len(SLAS.ledSectionAnimations)):
                SLAS.ledSectionAnimations[i] = animationsTaught[i]
            #SLAS.LedSectionAnimations([animationsTaught[0], animationsTaught[1]])
            SLAS.firstRun = [True]*len(SLAS.ledSections)
            logging.debug("Animations how set to be:" + str(SLAS.ledSectionAnimations))
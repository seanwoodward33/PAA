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

#Import other code
import SlasAnimations

#Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(asctime)s - (%(threadName)-10s) %(message)s')

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
        self.estops = [True, True, True]
        self.estopPositions = [[0,15],[42,56],[83,98]]
        self.doors = [True, True, True, True, True, True]
        self.doorPositions = [[0,5],[10,15],[20,25],[30,35],[40,45],[50,55]]
    
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
    
    def PrintLedSections(self):
        print (self.ledSections)
    
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

if __name__ == '__main__':
    logging.debug("Main SLAS control program running")
    
    logging.debug("Create SLAS workcell object")
    SLAS = Workcell()
    
    logging.debug("Create SLAS LED strip")
    SLAS.LedSetup(board.D18, 98, 1)
    
    logging.debug("Initialise LEDs")
    SLAS.LedInitialise()
    
    logging.debug("Setting up LED sections")
    SLAS.LedSections([[0,49],[50,98]])
    
    #Create list of all programmed animations to cycle through
    animationsTaught = ["RunComplete", "TeachMode", "EStop", "DoorOpen", "SystemRunningShort", "EStop", "SystemRunningLong"]
    logging.debug("Setting animation to be first two animations in animationsTaught list")
    SLAS.LedSectionAnimations([animationsTaught[0], animationsTaught[1]])
    
    
    logging.debug("Updating for all sections, forever loop times")
    x = 0
    while x < 1000:
        SLAS.UpdateBySection()
        SLAS.OutputLeds()
        x = x + 1
        if x == 950:
            x = 0
            animationsTaught = animationsTaught[1:] + animationsTaught[:1]
            for i in range(len(SLAS.ledSectionAnimations)):
                SLAS.ledSectionAnimations[i] = animationsTaught[i]
            #SLAS.LedSectionAnimations([animationsTaught[0], animationsTaught[1]])
            SLAS.firstRun = [True]*len(SLAS.ledSections)
            logging.debug("Animations how set to be:" + str(SLAS.ledSectionAnimations))

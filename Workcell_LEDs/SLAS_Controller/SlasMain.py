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
        pass
    
    def LedSetup(self, ledGpioPin, ledCount, ledBrightness, ledOrder = neopixel.GRB):
        self.ledPin = ledGpioPin
        self.ledCount = ledCount
        self.ledBrightness = ledBrightness
        self.ledOrder = ledOrder
        self.ledArray = np.zeros((ledCount,4))
        self.ledArray[:,3] = 1.0
        self.animationRun = True
        self.firstRun = True
        self.pulseDirection = "Down"
        self.time = datetime.datetime.now()
    
    def LedInitialise(self):
        self.ledStrip = neopixel.NeoPixel(self.ledPin, self.ledCount, brightness = self.ledBrightness, pixel_order=self.ledOrder, auto_write=False)
    
    def LedSections(self, sections = [[0,98]]):
        self.ledSections = sections
    
    def LedSectionAnimations(self, animations = ["RunComplete"]): #default runcomplete rainbow used
        self.ledSectionAnimations = animations
    
    def AnimationCall(self, input, section):
            method = getattr(self,input)
            return method(section)
    
    def PrintLedSections(self):
        print (self.ledSections)
    
    def UpdateBySection(self):
        for i in len(self.ledSections):
            section = self.ledSections[i]
            self.AnimationCall(self.ledSectionAnimations[i],section)
        if self.firstRun == True:
            self.firstRun = False
    
    def OutputLeds(self):
        for i in range(self.ledCount):
            x = np.rint(self.ledArray[i][0:3]*self.ledArray[i,3]).astype(int)
            self.ledStrip[i] = (x[0],x[1],x[2])
        self.ledStrip.show()        
    
    def RunComplete(self, section):
        SlasAnimations.RunComplete(self, section)
    
    def TeachMode(self, section):
        SlasAnimations.TeachMode(self, section)



if __name__ == '__main__':
    logging.debug("Main SLAS control program running")
    
    logging.debug("Create SLAS workcell object")
    SLAS = Workcell()
    
    logging.debug("Create SLAS LED strip")
    SLAS.LedSetup(board.D18, 98, 0.2)
    
    logging.debug("Initialise LEDs")
    SLAS.LedInitialise()
    
    logging.debug("Setting up LED sections")
    SLAS.LedSections([[0,49],[50,98]])
    
    logging.debug("Setting animation for each section")
    SLAS.LedSectionAnimations(["RunComplete", "TeachMode"])
    
    logging.debug("Testing RunComplete animation")
    SLAS.RunComplete(SLAS.ledSections[0])
    
    logging.debug("Update LEDs to see lights")
    SLAS.OutputLeds()
    
    logging.debug("Setting firstRun to False")
    SLAS.firstRun = False
    
    logging.debug("Looping through colours 500 times")
    for i in range(500):
        y = datetime.datetime.now()
        SLAS.RunComplete(SLAS.ledSections[0])
        SLAS.OutputLeds()
        while ((datetime.datetime.now() - y).microseconds * 1000) < 5000:
            pass
    
    logging.debug("Setting firstRun to True")
    SLAS.firstRun = True
    
    logging.debug("Testing TeachMode animation")
    SLAS.TeachMode(SLAS.ledSections[0])
    
    logging.debug("Update LEDs to see lights")
    SLAS.OutputLeds()
    
    logging.debug("Setting firstRun to False")
    SLAS.firstRun = False
    
    logging.debug("Pulsing lights 500 times")
    for i in range(500):
        y = datetime.datetime.now()
        SLAS.TeachMode(SLAS.ledSections[0])
        SLAS.OutputLeds()
        while ((datetime.datetime.now() - y).microseconds * 1000) < 1000:
            pass
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:06:26 2019

@author: Sean_Woodward
"""

import colorsys
import numpy as np
import logging
import datetime

"""Functions to control LEDs"""
#Non-normalised HSV to RGB function
def HsvToRgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

#Run complete - Run rainbow animation
def RunComplete(self, i):
    x = datetime.datetime.now()
    section = self.ledSections[i]
    #logging.debug("Rainbow animation. Time since last: " + str(x - self.time))
    self.time = x
    self.ledArray[section[0]:section[1]][:,3] = 1
    ledCount = len(self.ledArray[section[0]:section[1]])
    if self.firstRun[i] == True:
        for j in range(ledCount):
            for k in range(3):
                self.ledArray[section[0] + j][k] = HsvToRgb((((j)%(ledCount+1))/(ledCount)),1.0,1.0)[k]
        self.firstRun[i] = False
    
    if self.firstRun[i] == False:
        self.ledArray[section[0]:section[1]][:,0:3] = np.roll(self.ledArray[section[0]:section[1]][:,0:3],1, axis = 0)

#TeachMode - Pulse yellow
def TeachMode(self, i):
    x = datetime.datetime.now()
    #logging.debug("TeachMode animation. Time since last: " + str(x - self.time))
    self.time = x
    section = self.ledSections[i]
    self.ledArray[section[0]:section[1]][:,0:3] = [255,255,0]
    
    if self.firstRun[i] == True:
        self.ledArray[section[0]:section[1]][:,3] = 1
        if self.pulseDirection == "Up":
            self.pulseDirection = "Down"
        self.firstRun[i] = False
    
    if self.firstRun[i] == False:
        if self.pulseDirection == "Down":
            self.ledArray[section[0]:section[1]][:,3] = self.ledArray[section[0]:section[1]][:,3] - 0.01
            if self.ledArray[section[0]][3] <= 0.2:
                self.pulseDirection = "Up"
        if self.pulseDirection == "Up":
            self.ledArray[section[0]:section[1]][:,3] = self.ledArray[section[0]:section[1]][:,3] + 0.01
            if self.ledArray[section[0]][3] >= 1.0:
                self.pulseDirection = "Down"

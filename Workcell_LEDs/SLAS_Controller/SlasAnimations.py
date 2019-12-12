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
    section = self.ledSections[i]
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
    section = self.ledSections[i]
    self.ledArray[section[0]:section[1]][:,0:3] = [255,255,0]
   
    if self.firstRun[i] == True:
        self.ledArray[section[0]:section[1]][:,3] = self.ledBrightness
        self.pulseDirection = "Down"
        self.firstRun[i] = False
    
    if self.firstRun[i] == False:
        if self.pulseDirection == "Down":
            self.ledArray[section[0]:section[1]][:,3] = self.ledArray[section[0]:section[1]][:,3] - 0.01
            if self.ledArray[section[0]][3] <= self.dimLevelLeds:
                self.pulseDirection = "Up"
        if self.pulseDirection == "Up":
            self.ledArray[section[0]:section[1]][:,3] = self.ledArray[section[0]:section[1]][:,3] + 0.01
            if self.ledArray[section[0]][3] >= self.ledBrightness:
                self.pulseDirection = "Down"

#DoorOpen - Pulse purple
def DoorOpen(self, i):
    section = self.ledSections[i]
    self.ledArray[section[0]:section[1]][:,0:3] = [128,0,128]
    
    if self.firstRun[i] == True:
        self.ledArray[section[0]:section[1]][:,3] = self.ledBrightness
        self.pulseDirection = "Down"
        self.firstRun[i] = False
    
    if self.firstRun[i] == False:
        if self.pulseDirection == "Down":
            self.ledArray[section[0]:section[1]][:,3] = self.ledArray[section[0]:section[1]][:,3] - 0.01
            if self.ledArray[section[0]][3] <= self.dimLevelLeds:
                self.pulseDirection = "Up"
        if self.pulseDirection == "Up":
            self.ledArray[section[0]:section[1]][:,3] = self.ledArray[section[0]:section[1]][:,3] + 0.01
            if self.ledArray[section[0]][3] >= self.ledBrightness:
                self.pulseDirection = "Down"

#SystemRunningShort - Solid Green for short edges
def SystemRunningShort(self, i):
    section = self.ledSections[i]
    self.ledArray[section[0]:section[1]][:,0:3] = [0,255,0]
    
    if self.firstRun[i] == True:
        self.ledArray[section[0]:section[1]][:,3] = self.ledBrightness
        self.firstRun[i] = False
    
    if self.firstRun[i] == False:
        pass

#SystemRunningLong - Gradually growing Green for long edge
def SystemRunningLong(self, i):
    section = self.ledSections[i]
    self.ledArray[section[0]:section[1]][:,0:3] = [0,255,0]
    self.ledArray[section[0]:section[1]][:,3] = self.dimLevelLeds
    if self.firstRun[i] == True:
        if self.percentageComplete == 0:
            self.finishTime = datetime.datetime.now()+self.runLength
        if self.percentageComplete > 0:
            self.ledArray[section[0]:section[0]+round((self.percentageComplete*(section[1]-section[0])))][:,3]= self.ledBrightness
            self.finishTime = datetime.datetime.now()+(self.percentageComplete*self.runLength)        
        self.firstRun[i] = False
    
    if self.firstRun[i]  == False:
        self.percentageComplete = (self.finishTime - datetime.datetime.now())/self.runLength
        print (str(self.finishTime) + " " + str(datetime.datetime.now()) + " " + str(self.runLength) + " " + str(self.finishTime - datetime.datetime.now()) + " " + str(self.percentageComplete))
        if self.percentageComplete > 1:
            self.percentageComplete = 1
            self.LedSectionAnimations[i] = "RunComplete"
            self.percentageComplete = 0.0
        self.ledArray[section[0]:section[0]+round((self.percentageComplete*(section[1]-section[0])))][:,3]= self.ledBrightness
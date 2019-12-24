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
        logging.debug("Running RunComplete for first time. i value = " + str(i))
        if self.endRunPercentage == 0:
            self.endRunFinishTime = datetime.datetime.now()+self.endRunLength
        if self.endRunPercentage > 0:
            self.endRunFinishTime = datetime.datetime.now()+((1 - self.endRunPercentage) * self.endRunLength)
        for j in range(ledCount):
            for k in range(3):
                self.ledArray[section[0] + j][k] = HsvToRgb((((j)%(ledCount+1))/(ledCount)),1.0,1.0)[k]
        self.firstRun[i] = False
    
    if self.firstRun[i] == False:
        self.endRunPercentage = (self.endRunLength - (self.endRunFinishTime - datetime.datetime.now())) / self.endRunLength
        self.ledArray[section[0]:section[1]][:,0:3] = np.roll(self.ledArray[section[0]:section[1]][:,0:3],1, axis = 0)
        if self.endRunPercentage >= 1:
            #self.ledSectionAnimations[i] = "SystemRunningLong"
            self.ledSectionAnimations = ["SystemRunningLong","SystemRunningLong","SystemRunningLong"]
            self.endRunPercentage = 0.0
            #self.firstRun[i] = True
            self.firstRun = [True,True,True]
        self.ledArray[section[0]:section[1]][:,0:3] = np.roll(self.ledArray[section[0]:section[1]][:,0:3],1, axis = 0)
            

#SystemRunningLong - Gradually growing Green for long edge
def SystemRunningLong(self, i):
    section = self.ledSections[i]
    self.ledArray[section[0]:section[1]][:,0:3] = [0,255,0]
    self.ledArray[section[0]:section[1]][:,3] = self.dimLevelLeds
    if self.firstRun[i] == True:
        logging.debug("Running SystemRunningLong for first time. i value = " + str(i))
        if self.percentageComplete == 0:
            self.runFinishTime = datetime.datetime.now()+self.runLength
        if self.percentageComplete > 0:
            self.ledArray[section[0]:section[0]+round((self.percentageComplete*(section[1]-section[0])))][:,3] = self.ledBrightness
            self.runFinishTime = datetime.datetime.now() + ((1 - self.percentageComplete) * self.runLength)
        self.firstRun[i] = False
    
    if self.firstRun[i]  == False:
        self.percentageComplete = (self.runLength - (self.runFinishTime - datetime.datetime.now())) / self.runLength
        if self.percentageComplete >= 1:
            #self.ledSectionAnimations[i] = "RunComplete"
            self.ledSectionAnimations = ["RunComplete","RunComplete","RunComplete"]
            self.percentageComplete = 0.0
            #self.firstRun[i] = True
            self.firstRun = [True,True,True]
        self.ledArray[section[0]:section[0]+round((self.percentageComplete*(section[1]-section[0])))][:,3]= self.ledBrightness

#TeachMode - Pulse yellow
def TeachMode(self, i):
    section = self.ledSections[i]
    self.ledArray[section[0]:section[1]][:,0:3] = [255,255,0]
   
    if self.firstRun[i] == True:
        logging.debug("Running TeachMode for first time. i value = " + str(i))
        self.ledArray[section[0]:section[1]][:,3] = self.ledBrightness
        self.pulseDirection = "Down"
        self.firstRun[i] = False
    
    if self.firstRun[i] == False:
        if self.pulseDirection == "Down":
            self.ledArray[section[0]:section[1]][:,3] = self.ledArray[section[0]:section[1]][:,3] - 0.01
            if self.ledArray[section[0]][3] <= self.dimLevelLeds:
                #self.ledArray[section[0]:section[1]][:,3] = self.dimLevelLeds
                self.pulseDirection = "Up"
        if self.pulseDirection == "Up":
            self.ledArray[section[0]:section[1]][:,3] = self.ledArray[section[0]:section[1]][:,3] + 0.01
            if self.ledArray[section[0]][3] >= self.ledBrightness:
                #self.ledArray[section[0]:section[1]][:,3] = self.ledBrightness
                self.pulseDirection = "Down"

#DoorOpen - Pulse purple
def DoorOpen(self, i):
    section = self.ledSections[i]
    self.ledArray[section[0]:section[1]][:,0:3] = [128,0,128]
    
    if self.firstRun[i] == True:
        logging.debug("Running DoorOpen for first time. i value = " + str(i))
        self.ledArray[section[0]:section[1]][:,3] = self.ledBrightness
        self.pulseDirection = "Down"
        self.firstRun[i] = False
    
    if self.firstRun[i] == False:
        if self.pulseDirection == "Down":
            self.ledArray[section[0]:section[1]][:,3] = self.ledArray[section[0]:section[1]][:,3] - 0.01
            if self.ledArray[section[0]][3] <= self.dimLevelLeds:
                #self.ledArray[section[0]:section[1]][:,3] = self.dimLevelLeds
                self.pulseDirection = "Up"
        if self.pulseDirection == "Up":
            self.ledArray[section[0]:section[1]][:,3] = self.ledArray[section[0]:section[1]][:,3] + 0.01
            if self.ledArray[section[0]][3] >= self.ledBrightness:
                #self.ledArray[section[0]:section[1]][:,3] = self.ledBrightness
                self.pulseDirection = "Down"
    
    for j in range(len(self.doors)):
        if self.doors[j] == True:
            self.ledArray[self.doorPositions[j][0]:self.doorPositions[j][1]][:,0:3] = [255,255,0]

#TwoDoorOpen - White centre, Red nightrider left, Blue nightrider right
def TwoDoorOpen(self, i):
    section = self.ledSections[i]
    self.ledArray[section[0]:section[1]][:,0:3] = [255,255,255]
    
    if self.firstRun[i] == True:
        logging.debug("Running TwoDoorOpen for first time. i value = " + str(i))
        self.ledArray[section[0]:section[1]][:,3] = self.ledBrightness
        self.ledArray[section[0]:section[0]+self.twoDoorWidth][:,0:3] = self.twoDoorColours[i]
        self.pulseDirection = "Down"
        self.firstRun[i] = False
    
    if self.firstRun[i] == False:
        if self.pulseDirection == "Down":
            self.ledArray[section[0]:section[1]][:,0:3] = np.roll(self.ledArray[section[0]:section[1]][:,0:3],1, axis = 0)
            if self.ledArray[section[1]][:,0:3] == self.twoDoorColours[i]:
                self.pulseDirection = "Up"
                
        if self.pulseDirection == "Up":
            self.ledArray[section[0]:section[1]][:,0:3] = np.roll(self.ledArray[section[0]:section[1]][:,0:3],-1, axis = 0)
            if self.ledArray[section[0]][:,0:3] == self.twoDoorColours[i]:
                self.pulseDirection = "Down"
"""
    for j in range(len(self.doors)):
        if self.doors[j] == True:
            self.ledArray[self.doorPositions[j][0]:self.doorPositions[j][1]][:,0:3] = [255,255,0]
"""
#SystemRunningShort - Solid Green for short edges
def SystemRunningShort(self, i):
    section = self.ledSections[i]
    self.ledArray[section[0]:section[1]][:,0:3] = [0,255,0]
    
    if self.firstRun[i] == True:
        logging.debug("Running SystemRunningShort for first time. i value = " + str(i))
        self.ledArray[section[0]:section[1]][:,3] = self.ledBrightness
        self.firstRun[i] = False
    
    if self.firstRun[i] == False:
        pass


#EStop - Pulse Red
def EStop(self, i):
    section = self.ledSections[i]
    self.ledArray[section[0]:section[1]][:,0:3] = [255,0,0]
    
    if self.firstRun[i] == True:
        logging.debug("Running EStop for first time. i value = " + str(i))
        self.ledArray[section[0]:section[1]][:,3] = self.ledBrightness
        self.pulseDirection = "Down"
        self.firstRun[i] = False
    
    if self.firstRun[i] == False:
        if self.pulseDirection == "Down":
            self.ledArray[section[0]:section[1]][:,3] = self.ledArray[section[0]:section[1]][:,3] - 0.01
            if self.ledArray[section[0]][3] <= self.dimLevelLeds:
                #self.ledArray[section[0]:section[1]][:,3] = self.dimLevelLeds
                self.pulseDirection = "Up"
        if self.pulseDirection == "Up":
            self.ledArray[section[0]:section[1]][:,3] = self.ledArray[section[0]:section[1]][:,3] + 0.01
            if self.ledArray[section[0]][3] >= self.ledBrightness:
                #self.ledArray[section[0]:section[1]][:,3] = self.ledBrightness
                self.pulseDirection = "Down"
    
    for j in range(len(self.estops)):
        if self.estops[j] == True:
            self.ledArray[self.estopPositions[j][0]:self.estopPositions[j][1]][:,0:3] = [255,255,0]
            #self.ledArray[self.estopPositions[j][0]:self.estopPositions[j][1]][:,3] = self.ledBrightness
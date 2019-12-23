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
import colorsys
import RPi.GPIO as GPIO
import digitalio


#Import other code
import SlasAnimations

#Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(asctime)s - (%(threadName)-10s) %(message)s')

#Define workcell class
class Workcell(threading.Thread):
    def __init__(self):
        logging.debug("Starting Workcell thread")
        self.animationRun = True
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
        self.lastRunState = ["SystemRunningShort", "SystemRunningLong", "SystemRunningShort"]
        self.estops = [False, False, False]
        self.estopPositions = [[0,2],[46,48],[96,98]] # Testing board
        #self.estopPositions = [[0,5],[46,56],[293,302]] # SLAS Workcell
        self.doors = [False, False, False, False, False, False]
        self.doorPositions = [[3,10],[15,22],[36,43],[44,50],[75,83],[88,95]] #Testing board
        #self.doorPositions = [[6,45],[55,100],[117,232],[117,232],[248,292],[303,344]] #SLAS Workcell
        
        self.LedSetup(board.D18, 98, 1) #When running on test board
        #SLAS.LedSetup(board.D18, 348, 1) #When running on SLAS workcell
        self.LedInitialise()
        self.LedSections([[0,21],[21,63],[63,98]])
        #SLAS.LedSections([[0,110],[111,238],[239,348]]) #When running on SLAS workcell #Section 1 - [0,110], section 2 - [111,238], section 3 =- [239,348]
        #self.LedAnimationsTaught(["RunComplete", "TeachMode", "EStop", "DoorOpen", "SystemRunningShort", "EStop", "SystemRunningLong"])
        #self.LedSectionAnimations([self.animationsTaught[0], self.animationsTaught[1], self.animationsTaught[2]])
        self.LedSectionAnimations(["SystemRunningShort", "SystemRunningLong", "SystemRunningShort"])
        self.RunLoop()

    def LedSetup(self, ledGpioPin, ledCount, ledBrightness, ledOrder = neopixel.GRB):
        logging.debug("LedSetup Running")
        self.ledPin = ledGpioPin
        self.ledCount = ledCount
        self.ledBrightness = ledBrightness
        self.ledOrder = ledOrder
        self.ledArray = np.zeros((ledCount,4))
        self.ledArray[:,3] = self.ledBrightness
    
    def LedInitialise(self):
        logging.debug("LEDs initialised")
        self.ledStrip = neopixel.NeoPixel(self.ledPin, self.ledCount, brightness = self.ledBrightness, pixel_order=self.ledOrder, auto_write=False)
    
    def LedSections(self, sections = [[0,98]]):
        logging.debug("LED sections defined")
        self.ledSections = sections
        self.firstRun = [True]*len(self.ledSections)
    
    def PrintTest(self):
        logging.debug("Test")

    def LedAnimationsTaught(self, animations = ["RunComplete"]): #default runcomplete rainbow used
        logging.debug("LED animations taught taught")
        self.animationsTaught = animations
    
    def LedSectionAnimations(self, animations = ["RunComplete"]): #default runcomplete rainbow used
        logging.debug("LED animations to use sorted")
        self.ledSectionAnimations = animations
    
    def AnimationCall(self, input, section):
            method = getattr(self,input)
            return method(section)
    
    def UpdateBySection(self):
       #logging.debug("Updating the LED sections")
        for i in range(len(self.ledSections)):
            self.AnimationCall(self.ledSectionAnimations[i], i)
    
    def OutputLeds(self):
        #logging.debug("Outputting LED values")
        for i in range(self.ledCount):
            x = np.rint(self.ledArray[i][0:3]*self.ledArray[i,3]).astype(int)
            self.ledStrip[i] = (x[0],x[1],x[2])
        self.ledStrip.show()
    
    def QueueCheck(self):
        if runQ.empty() == False:
            queue = runQ.get()

            if queue == [0,0,0,0,0,0,0,0]:
                self.estops = [False, False, False]
                self.doors = [False, False, False, False, False, False]
                self.ledSectionAnimations = self.lastRunState
            
            if queue[0] == True or queue[1] == True or queue[2] == True:
                self.estops = queue[0:3]
                self.ledSectionAnimations = ["EStop","EStop","EStop"]
            
    def RunLoop(self):
        logging.debug("Starting Workcell running loop")
        while self.animationRun == True:
            self.QueueCheck()
            self.UpdateBySection()
            self.QueueCheck()
            self.OutputLeds()
    
    def RunComplete(self, i):
        self.lastRunState[i] = "RunComplete"
        SlasAnimations.RunComplete(self, i)
    
    def TeachMode(self, i):
        SlasAnimations.TeachMode(self, i)

    def DoorOpen(self, i):
        SlasAnimations.DoorOpen(self, i)
    
    def SystemRunningShort(self, i):
        self.lastRunState[i] = "SystemRunningShort"
        SlasAnimations.SystemRunningShort(self, i)
    
    def SystemRunningLong(self, i):
        self.lastRunState[i] = "SystemRunningLong"
        SlasAnimations.SystemRunningLong(self, i)
    
    def EStop(self,i):
        SlasAnimations.EStop(self,i)
        
#Define SafetySystem Class
class SafetySystem(threading.Thread):
    def __init__(self):
        #threading.Thread.__init__(self)
        logging.debug("Starting SafetySystem thread")
        self.doors = [0,0,0,0,0,0,0,0]
        self.lastDoors =[0,0,0,0,0,0,0,0]
        self.pin = digitalio.DigitalInOut(board.D4)
        self.pin.direction = digitalio.Direction.INPUT
        self.pin.pull = digitalio.Pull.DOWN
        self.checking()
    
    def checking(self):
        logging.debug("Starting SafetySystem checking loop")
        while True:
            self.doors[0] = self.pin.value
            if self.doors[0] != self.lastDoors[0]:
                logging.debug("Change in self.doors")
                while runQ.empty() == False:
                    runQ.get()
                runQ.put(self.doors)
            self.lastDoors[0] = self.doors[0]
            time.sleep(0.5)

#Setup pins for RGB filter LEDs
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

GPIO.output(11, GPIO.HIGH)
GPIO.output(12, GPIO.HIGH)
GPIO.output(13, GPIO.HIGH)

redPin = GPIO.PWM(11, 1000)
greenPin = GPIO.PWM(12, 1000)
bluePin = GPIO.PWM(13, 1000)

rgbPwmValues = (1,0,0)

redPin.start(rgbPwmValues[0])
greenPin.start(rgbPwmValues[1])
bluePin.start(rgbPwmValues[2])


def RgbCycle(i):
    i = colorsys.rgb_to_hsv(i[0],i[1],i[2])
    i = colorsys.hsv_to_rgb((i[0]+0.01)%1, 1, 1)
    return i


if __name__ == '__main__':
    #Define queue to pass between threads    
    runQ = queue.Queue()

    #Establish Workcell and SafetySystem workcell
    threading.Thread(target = Workcell).start()
    threading.Thread(target = SafetySystem).start()
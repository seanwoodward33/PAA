#!/usr/bin/python3
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
        self.dimLevelLeds = 0.1
        self.runTime = datetime.datetime.now()
        self.runFinishTime = datetime.datetime.now()
        self.percentageComplete = 0.0
        self.runLength= datetime.timedelta(seconds = 60)
        self.endRunTime = datetime.datetime.now()
        self.endRunFinishTime = datetime.datetime.now()
        self.endRunPercentage = 0.0
        self.endRunLength= datetime.timedelta(seconds = 10)
        self.lastRunState = ["SystemRunningLong", "SystemRunningLong", "SystemRunningLong"]
        self.estops = [False, False, False]
        #self.estopPositions = [[0,2],[46,48],[96,98]] # Testing board
        self.estopPositions = [[0,5],[46,56],[293,302]] # SLAS Workcell
        self.doors = [False, False, False, False, False, False]
        #self.doorPositions = [[3,10],[15,22],[36,43],[44,50],[75,83],[88,95]] #Testing board
        self.doorPositions = [[6,45],[55,100],[117,232],[117,232],[248,292],[303,344]] #SLAS Workcell
        self.twoDoorColours = [[255,0,0], [255,255,255],[0,0,255]]
        self.twoDoorWidth = 5
        self.animationDirection = ["Right","Right","Right"]
       
        
        """Setting up system to run"""
        #self.LedSetup(board.D18, 98, 1) #When running on test board
        self.LedSetup(board.D18, 348, 1) #When running on SLAS workcell
        self.LedInitialise()
        #self.LedSections([[0,21],[21,63],[63,98]])
        self.LedSections([[0,110],[111,238],[239,348]]) #When running on SLAS workcell #Section 1 - [0,110], section 2 - [111,238], section 3 =- [239,348]
        #self.LedAnimationsTaught(["RunComplete", "TeachMode", "EStop", "DoorOpen", "SystemRunningShort", "EStop", "SystemRunningLong"])
        #self.LedSectionAnimations([self.animationsTaught[0], self.animationsTaught[1], self.animationsTaught[2]])
        #self.LedSectionAnimations(["TwoDoorOpen", "TwoDoorOpen", "TwoDoorOpen"])
        self.LedSectionAnimations(["SystemRunningLong", "SystemRunningLong", "SystemRunningLong"])
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
            logging.debug("Change in safetySystem state detected.")
            queue = runQ.get()
            logging.debug("Queue read to be: " + str(queue))
            #Safety system treats high as safe, code treats low as safe
            queue = [not i for i in queue]
            logging.debug("Negated queue is: " + str(queue))
            
            #While ignoring doors
            #queue[3:] = [0,0,0,0,0,0]

            if queue == [0,0,0,0,0,0,0,0,0]:
                self.estops = [False, False, False]
                self.doors = [False, False, False, False, False, False]
                self.ledSectionAnimations = self.lastRunState
                self.firstRun = [True]*len(self.ledSections)
                
                """
                for i in range(len(self.ledSectionAnimations)):
                    if self.ledSectionAnimations[i] == "RunComplete":
                       self.firstRun[i] = True
                """
                
            if queue[3] == True or queue[4] == True or queue[5] == True or queue[6] == True or queue[7] == True or queue[8] == True:
                self.doors = queue[3:]
                self.ledSectionAnimations = ["DoorOpen","DoorOpen","DoorOpen"]
                """
                if sum(queue[3:]) > 1:
                    self.ledSectionAnimations = ["TwoDoorOpen","TwoDoorOpen","TwoDoorOpen"]
                """
                self.firstRun = [True]*len(self.ledSections)
                
            if queue[0] == True or queue[1] == True or queue[2] == True:
                self.estops = queue[0:3]
                self.ledSectionAnimations = ["EStop","EStop","EStop"]
                self.firstRun = [True]*len(self.ledSections)

            
            
    def RunLoop(self):
        logging.debug("Starting Workcell running loop")
        while self.animationRun == True:
            self.QueueCheck()
            self.UpdateBySection()
            self.OutputLeds()
    
    def RunComplete(self, i):
        rgbQ.put("Rainbow")
        self.lastRunState[i] = "RunComplete"
        SlasAnimations.RunComplete(self, i)
    
    def TeachMode(self, i):
        SlasAnimations.TeachMode(self, i)

    def DoorOpen(self, i):
        rgbQ.put("Purple")
        SlasAnimations.DoorOpen(self, i)
    
    def TwoDoorOpen(self, i):
        rgbQ.put("White")
        SlasAnimations.TwoDoorOpen(self, i)
    
    def SystemRunningShort(self, i):
        rgbQ.put("Green")
        self.lastRunState[i] = "SystemRunningShort"
        SlasAnimations.SystemRunningShort(self, i)
    
    def SystemRunningLong(self, i):
        rgbQ.put("Green")
        self.lastRunState[i] = "SystemRunningLong"
        SlasAnimations.SystemRunningLong(self, i)
    
    def EStop(self,i):
        rgbQ.put("Red")
        SlasAnimations.EStop(self,i)
        
#Define SafetySystem Class
class SafetySystem(threading.Thread):
    def __init__(self):
        #threading.Thread.__init__(self)
        logging.debug("Starting SafetySystem thread")
        self.doors = [1,1,1,1,1,1,1,1,1] #High/True equals safe
        self.lastDoors =[1,1,1,1,1,1,1,1,1] #High/True equals safe
        
        self.estop1 = digitalio.DigitalInOut(board.D2)
        self.estop1.direction = digitalio.Direction.INPUT
        self.estop1.pull = digitalio.Pull.DOWN
        self.estop2 = digitalio.DigitalInOut(board.D3)
        self.estop2.direction = digitalio.Direction.INPUT
        self.estop2.pull = digitalio.Pull.DOWN
        self.estop3 = digitalio.DigitalInOut(board.D4)
        self.estop3.direction = digitalio.Direction.INPUT
        self.estop3.pull = digitalio.Pull.DOWN
        self.door1 = digitalio.DigitalInOut(board.D5)
        self.door1.direction = digitalio.Direction.INPUT
        self.door1.pull = digitalio.Pull.DOWN
        self.door2 = digitalio.DigitalInOut(board.D6)
        self.door2.direction = digitalio.Direction.INPUT
        self.door2.pull = digitalio.Pull.DOWN
        self.door3 = digitalio.DigitalInOut(board.D7)
        self.door3.direction = digitalio.Direction.INPUT
        self.door3.pull = digitalio.Pull.DOWN
        self.door4 = digitalio.DigitalInOut(board.D8)
        self.door4.direction = digitalio.Direction.INPUT
        self.door4.pull = digitalio.Pull.DOWN
        self.door5 = digitalio.DigitalInOut(board.D9)
        self.door5.direction = digitalio.Direction.INPUT
        self.door5.pull = digitalio.Pull.DOWN
        self.door6 = digitalio.DigitalInOut(board.D10)
        self.door6.direction = digitalio.Direction.INPUT
        self.door6.pull = digitalio.Pull.DOWN
        self.Checking()
    
    def Checking(self):
        logging.debug("Starting SafetySystem checking loop")
        while True:
            self.doors[0] = self.estop1.value
            self.doors[1] = self.estop2.value
            self.doors[2] = self.estop3.value
            self.doors[3] = self.door1.value
            self.doors[4] = self.door2.value
            self.doors[5] = self.door3.value
            self.doors[6] = self.door4.value
            self.doors[7] = self.door5.value
            self.doors[8] = self.door6.value
            
            for i in range(len(self.doors)):
                if self.doors[i] != self.lastDoors[i]:
                    #logging.debug("Change in inputs")
                    logging.debug("Doors string = " + str(self.doors))
                    while runQ.empty() == False:
                        runQ.get()
                    runQ.put(self.doors)
                    self.lastDoors[i] = self.doors[i]
 
#Define RGB Class for dumb lights
class RgbLights(threading.Thread):
    def __init__(self):
        logging.debug("Starting RGBLights thread")
        #Setup pins for RGB filter LEDs
        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)

        GPIO.output(11, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)

        """
        self.redPin = GPIO.PWM(11, 1000)
        self.greenPin = GPIO.PWM(12, 1000)
        self.bluePin = GPIO.PWM(13, 1000)

        self.rgbPwmValues = (0,0,1)
        
        self.redPin.start(50)
        self.greenPin.start(50)
        self.bluePin.start(50)
        """

        """
        self.redPin.start(self.rgbPwmValues[0]*100)
        self.greenPin.start(self.rgbPwmValues[1]*100)
        self.bluePin.start(self.rgbPwmValues[2]*100)
        """
        #self.rgbColour = "Green"
        
        #self.Running()
        
    def UpdatePins(self):
        self.redPin.ChangeDutyCycle(self.rgbPwmValues[0]*100)
        self.greenPin.ChangeDutyCycle(self.rgbPwmValues[1]*100)
        self.bluePin.ChangeDutyCycle(self.rgbPwmValues[2]*100)
        
    def RgbRed(self):
        self.rgbPwmValues = (1,0,0)
        self.UpdatePins()
        
    def RgbGreen(self):
        self.rgbPwmValues = (0,1,0)
        self.UpdatePins()

    def RgbPurple(self):
        self.rgbPwmValues = (0.5,0,0.5)
        self.UpdatePins()

    def RgbWhite(self):
        self.rgbPwmValues = (1,1,1)
        self.UpdatePins()

    def RgbRainbow(self):
        i = self.rgbPwmValues
        i = colorsys.rgb_to_hsv(i[0],i[1],i[2])
        self.rgbPwmValues = colorsys.hsv_to_rgb((i[0]+0.01)%1, 1, 1)
        self.UpdatePins()

    def Running(self):
        while True:
            if rgbQ.empty() == False:   
                self.rgbColour = rgbQ.get()
                
            if self.rgbColour == "Green":
                self.RgbGreen()
            
            if self.rgbColour == "Red":
                self.RgbRed()
            
            if self.rgbColour == "Purple":
                self.RgbPurple()
            
            if self.rgbColour == "White":
                self.RgbWhite()
        
            if self.rgbColour == "Rainbow":
                self.RgbRainbow()    
        

"""     
def RgbRed():
    rgbPwmValues = (1,0,0)
    redPin.ChangeDutyCycle(rgbPwmValues[0])
    greenPin.ChangeDutyCycle(rgbPwmValues[1])
    bluePin.ChangeDutyCycle(rgbPwmValues[2])

def RgbGreen():
    rgbPwmValues = (0,1,0)
    redPin.ChangeDutyCycle(rgbPwmValues[0])
    greenPin.ChangeDutyCycle(rgbPwmValues[1])
    bluePin.ChangeDutyCycle(rgbPwmValues[2])

def RgbPurple():
    rgbPwmValues = (0.5,0,0.5)
    redPin.ChangeDutyCycle(rgbPwmValues[0])
    greenPin.ChangeDutyCycle(rgbPwmValues[1])
    bluePin.ChangeDutyCycle(rgbPwmValues[2])

def RgbWhite():
    rgbPwmValues = (1,1,1)
    redPin.ChangeDutyCycle(rgbPwmValues[0])
    greenPin.ChangeDutyCycle(rgbPwmValues[1])
    bluePin.ChangeDutyCycle(rgbPwmValues[2])

def RgbRainbow(i):
    i = colorsys.rgb_to_hsv(i[0],i[1],i[2])
    rgbPwmValues = colorsys.hsv_to_rgb((i[0]+0.01)%1, 1, 1)
    redPin.ChangeDutyCycle(rgbPwmValues[0])
    greenPin.ChangeDutyCycle(rgbPwmValues[1])
    bluePin.ChangeDutyCycle(rgbPwmValues[2])
    return i

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

rgbPwmValues = (0,1,0)
rgbColour = "Green"

redPin.start(rgbPwmValues[0])
greenPin.start(rgbPwmValues[1])
bluePin.start(rgbPwmValues[2])
"""

if __name__ == '__main__':
    #Define queue to pass between threads    
    runQ = queue.Queue()
    rgbQ = queue.Queue()

    #Establish Workcell and SafetySystem workcell
    threading.Thread(target = Workcell).start()
    threading.Thread(target = SafetySystem).start()
    threading.Thread(target = RgbLights).start()
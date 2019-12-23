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
        #threading.Thread.__init__(self)
        logging.debug("Starting Workcell thread")
        #self.q = queue.Queue()
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
        self.estops = [False, False, False]
        self.estopPositions = [[0,2],[46,48],[96,98]] # Testing board
        #self.estopPositions = [[0,5],[46,56],[293,302]] # SLAS Workcell
        self.doors = [False, False, False, False, False, False]
        self.doorPositions = [[3,10],[15,22],[36,43],[44,50],[75,83],[88,95]] #Testing board
        #self.doorPositions = [[6,45],[55,100],[117,232],[117,232],[248,292],[303,344]] #SLAS Workcell
        #super(Workcell, self).__init__()
        
        self.LedSetup(board.D18, 98, 1) #When running on test board
        self.LedInitialise()
        self.LedSections([[0,30],[30,60],[60,98]])
        self.LedAnimationsTaught(["RunComplete", "TeachMode", "EStop", "DoorOpen", "SystemRunningShort", "EStop", "SystemRunningLong"])
        self.LedSectionAnimations([self.animationsTaught[0], self.animationsTaught[1], self.animationsTaught[2]])
        self.RunLoop()
        
        
        
    """
    def OnThread(self, function, *args, **kwargs):
        self.q.put((function, args, kwargs))
    
    def run(self):
        while True:
            try:
                function, args, kwargs = self.q.get(timeout = 0.01)
                function (*args, **kwargs)
            except queue.Empty:
                self.idle()
    
    def idle(self):
            pass
    
    """
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
        #logging.debug("Checking the LED queue")
        if runQ.empty() == False:
            runQ.get()
            self.animationsTaught = self.animationsTaught[1:] + self.animationsTaught[:1]
            self.ledSectionAnimations = [self.animationsTaught[0],self.animationsTaught[1],self.animationsTaught[2]]
            self.firstRun = [True]*len(SLAS.ledSections)
            
    def RunLoop(self):
        logging.debug("Starting Workcell running loop")
        while self.animationRun == True:
            self.QueueCheck()
            self.UpdateBySection()
            self.QueueCheck()
            self.OutputLeds()
    
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
        
#Define SafetySystem Class
class SafetySystem(threading.Thread):
    def __init__(self):
        #threading.Thread.__init__(self)
        logging.debug("Starting SafetySystem thread")
        self.doors = [0]
        self.lastDoors =[0]
        self.pin = digitalio.DigitalInOut(board.D4)
        self.pin.direction = digitalio.Direction.INPUT
        self.pin.pull = digitalio.Pull.DOWN
    
    def checking(self):
        logging.debug("Starting SafetySstem checking loop")
        while True:
            self.doors[0] = self.pin.value
            if self.doors[0] != self.lastDoors[0]:
                print("Change in self.doors")
                while runQ.empty() == False:
                    runQ.get()
                runQ.put(self.doors[0])
            self.lastDoors[0] = self.doors[0]

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
    
    runQ = queue.Queue()
    
    #SLAS = Workcell()
    #SLAS.start()
    #SLAS = threading.Thread(target = Workcell)
    #SLAS.start()
    #safety = SafetySystem()
    
    threading.Thread(target = Workcell).start()

    #threading.Thread(target = SLAS).start()
    #time.sleep(1)
    #SLAS.OnThread(SLAS.PrintTest())
    #SLAS.OnThread(SLAS.LedSetup(board.D18, 98, 1))
    #SLAS.OnThread(SLAS.LedInitialise())
    #SLAS.OnThread(SLAS.LedSections([[0,30],[30,60],[60,98]]))
    #animationsTaught = ["RunComplete", "TeachMode", "EStop", "DoorOpen", "SystemRunningShort", "EStop", "SystemRunningLong"]
    #SLAS.OnThread(SLAS.LedAnimationsTaught(animationsTaught))
    #SLAS.OnThread(SLAS.LedSectionAnimations([animationsTaught[0], animationsTaught[1], animationsTaught[2]]))
    #SLAS.OnThread(SLAS.RunLoop())
    #SLAS.start()    
    #SLAS.LedSetup(board.D18, 98, 1) #When running on test board
    #SLAS.LedInitialise()
    #SLAS.LedSections([[0,30],[30,60],[60,98]])
    #SLAS.LedAnimationsTaught(["RunComplete", "TeachMode", "EStop", "DoorOpen", "SystemRunningShort", "EStop", "SystemRunningLong"])
    #SLAS.LedSectionAnimations([SLAS.animationsTaught[0], SLAS.animationsTaught[1],SLAS.animationsTaught[2]])
    #SLAS.RunLoop()
    
    #threading.Thread(target = safety).start()
    #safety.start()
    #safety.checking()
    #SLAS.animationRun = False
    
    #x = 0
    
    #while x < 2000:
     #   x = x+1
"""
        redPin.ChangeDutyCycle(rgbPwmValues[0]*100)
        greenPin.ChangeDutyCycle(rgbPwmValues[1]*100)
        bluePin.ChangeDutyCycle(rgbPwmValues[2]*100)
        
        rgbPwmValues = RgbCycle(rgbPwmValues)
"""
      #  if x == 1950:
       #     x = 0
            
"""
            animationsTaught = animationsTaught[1:] + animationsTaught[:1]
            for i in range(len(SLAS.ledSectionAnimations)):
                SLAS.ledSectionAnimations[i] = animationsTaught[i]
            SLAS.firstRun = [True]*len(SLAS.ledSections)
"""
"""
    logging.debug("Main SLAS control program running")
    
    logging.debug("Create SLAS workcell object")
    SLAS = Workcell()
    
    logging.debug("Create SLAS LED strip")
    SLAS.LedSetup(board.D18, 98, 1) #When running on test board
    #SLAS.LedSetup(board.D18, 348, 1) #When running on SLAS workcell
    
    logging.debug("Initialise LEDs")
    SLAS.LedInitialise()
    
    logging.debug("Setting up LED sections")
    SLAS.LedSections([[0,30],[30,60],[60,98]]) #Testing board
    #SLAS.LedSections([[0,110],[111,238],[239,348]]) #Section 1 - [0,110], section 2 - [111,238], section 3 =- [239,348]
    
    #Create list of all programmed animations to cycle through
    animationsTaught = ["RunComplete", "TeachMode", "EStop", "DoorOpen", "SystemRunningShort", "EStop", "SystemRunningLong"]
    logging.debug("Setting animation to be first two animations in animationsTaught list")
    SLAS.LedSectionAnimations([animationsTaught[0], animationsTaught[1],animationsTaught[2]])
    logging.debug("Animations now set to be:" + str(SLAS.ledSectionAnimations))
    
    
    logging.debug("Updating for all sections, forever loop times")
    x = 0
    while x < 2000:
        SLAS.UpdateBySection()
        SLAS.OutputLeds()
        x = x + 1
        
        redPin.ChangeDutyCycle(rgbPwmValues[0]*100)
        greenPin.ChangeDutyCycle(rgbPwmValues[1]*100)
        bluePin.ChangeDutyCycle(rgbPwmValues[2]*100)
        
        rgbPwmValues = RgbCycle(rgbPwmValues)
        
        if x == 1950:
            x = 0
            animationsTaught = animationsTaught[1:] + animationsTaught[:1]
            for i in range(len(SLAS.ledSectionAnimations)):
                SLAS.ledSectionAnimations[i] = animationsTaught[i]
            SLAS.firstRun = [True]*len(SLAS.ledSections)
            logging.debug("Animations now set to be:" + str(SLAS.ledSectionAnimations))
"""
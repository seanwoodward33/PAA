# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 11:13:04 2019

@author: sean_woodward
"""

#Import libraries
import threading
import queue
import time
import logging

#Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(asctime)s - (%(threadName)-10s) %(message)s')

#Import Pi_LED_Controller from seperate file
import Pi_LED_Controller as PiCont
import animations

#
class animationClass():
    def __init__(self):
        logging.debug("Starting animationClass")
        while runQ.empty() == False:
            logging.debug(runQ.get())
        self.QueueGet()
        logging.debug("Exiting animationClass")
    
    def QueueGet(self):
        self.AnimationName(animationNameQ.get())
    
    def AnimationName(self, input):
        method = getattr(self,input)
        logging.debug("Method called: " + input)
        return method()

    def Rainbow(self):
        animations.Rainbow(ledStrip, q = runQ, numOfLoops = 10)
    
    def ColourWipe(self):
        animations.ColourWipe(ledStrip, (255,0,255), int(1000/len(ledStrip)), q = runQ)
    
    def Shutdown(self):
        animations.ColourWipe(ledStrip, (0,0,0), int(1000/len(ledStrip)), q = runQ)

#Default run program
if __name__ == '__main__':
    #Set up LED strip
    ledStrip = PiCont.LedSetup()
    
    #Set up queues for passing between threads
    runQ = queue.Queue()
    animationNameQ = queue.Queue()
    animationArgsQ = queue.Queue()

    #Set up default run
    animationNameQ.put("Rainbow")
    
    #Start Flask thread
    threading.Thread(target = animationClass, name = "First ani").start()
    
    #Run
    time.sleep(15)
    animationNameQ.put("Rainbow")
    runQ.put("stop")
    time.sleep(1)
    threading.Thread(target = animationClass).start()
    time.sleep(3)
    animationNameQ.put("ColourWipe")
    runQ.put("stop")
    time.sleep(1)
    threading.Thread(target = animationClass).start()    
    time.sleep(3)
    animationNameQ.put("Rainbow")
    runQ.put("stop")
    time.sleep(1)
    threading.Thread(target = animationClass).start()
    time.sleep(3)
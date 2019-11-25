# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:03:32 2019

@author: sean_woodward
"""

#Import libraries
import threading
import queue
import time
import logging
import board

#Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(asctime)s - (%(threadName)-10s) %(message)s')

#Import libraries for Flask server
from flask import Flask, request
from flask_restful import Resource, Api

#Import Pi_LED_Controller from seperate file
import Pi_LED_Controller as PiCont
import animations

#Setup flask server
app = Flask(__name__)
api = Api(app)

#Define classes for flask
class Rainbow(Resource):
    def get(self):
        animationNameQ.put("Rainbow")
        #animationArgsQ.put("")
        runQ.put("stop")
        time.sleep(0.1)
        threading.Thread(target = animationClass).start()

class ColourWipe(Resource):
    def get(self):
        animationNameQ.put("ColourWipe")
        #animationArgsQ.put("")
        runQ.put("stop")
        time.sleep(0.1)
        threading.Thread(target = animationClass).start()

class Shutdown(Resource):
    def get(self):
        animationNameQ.put("Shutdown")
        #animationArgsQ.put("")
        runQ.put("stop")
        time.sleep(0.1)
        threading.Thread(target = animationClass).start()
        
        
#Add functions to web address
api.add_resource(Rainbow, '/rainbow')
api.add_resource(ColourWipe, '/colourwipe')
api.add_resource(Shutdown, '/shutdown')

#Define functions for threading
def flaskThread():
    logging.debug("Starting flaskThread")
    threading.Thread(target = animationClass, name = "First ani").start()
    app.run(host = '0.0.0.0', port = '5002')
    logging.debug("Stopping flaskThread")
    
class animationClass(threading.Thread):
    def __init__(self):#, ledStrip):
        logging.debug("Starting animationClass")
        self.ledStrip = ledStrip1
        while runQ.empty() == False:
            logging.debug("Clearing Queue")
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
        animations.Rainbow(ledStrip1, q = runQ)
    
    def ColourWipe(self):
        animations.ColourWipe(ledStrip1, (255,0,255), waitTime = int(1000/len(ledStrip1)), q = runQ)
    
    def Shutdown(self):
        animations.ColourWipe(ledStrip1, (0,0,0), waitTime = int(1000/len(ledStrip1)), q = runQ)

#Default run program
if __name__ == '__main__':
    #Set up LED strip
    ledStrip1 = PiCont.LedSetup(ledCount = 98, ledPin = board.D18)
    #ledStrip2 = PiCont.LedSetup(ledCount = 51, ledPin = board.D12)
    
    #Set up queues for passing between threads
    runQ = queue.Queue()
    animationNameQ = queue.Queue()
    animationArgsQ = queue.Queue()

    #Set up default run
    animationNameQ.put("Rainbow")
    #animationNameQ.put("Rainbow")
    
    #Start Flask thread
    threading.Thread(target = animationClass).start()
    #threading.Thread(target = animationClass, args = (ledStrip2,)).start()
    app.run(host = '0.0.0.0', port = '5002')
    #threading.Thread(target = flaskThread, name = "flaskThread").start()
    
    """
    #Start animation thread
    t = threading.Thread(target = animationThread)
    t.start()
    """
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:03:32 2019

@author: sean_woodward
"""
#Import libraries
import threading

#Import libraries for Flask server
from flask import Flask, request
from flask_restful import Resource, Api
#from json import dumps
#from flask.ext.jsonpify import jsonify

#Import Pi_LED_Controller from seperate file
import Pi_LED_Controller as PiCont
import animations

#Setup flask server
app = Flask(__name__)
api = Api(app)

#Define classes for flask
class Rainbow(Resource):
    def get(self):
        t.stop()
        t.start()
        t.Animation("Rainbow")
        #animations.Rainbow(ledStrip, numOfLoops = 10)

class Pixelwipe(Resource):
    def get(self):
        animations.PixelWipe(ledStrip,(255,0,255))

class Shutdown(Resource):
    def get(self):
        t._stop()
        t.start()
        t.Animation("ColourWipe")
        
        
#Add functions to web address
api.add_resource(Rainbow, '/rainbow')
api.add_resource(Pixelwipe, '/pixelwipe')
api.add_resource(Shutdown, '/shutdown')

#Define functions for threading
def flaskThread():
    app.run(host = '0.0.0.0', port = '5002')

class animationThread():
    def __init__(self):
        pass
    
    def Animation(self, input):
        method = getattr(self,input)
        return method()
    
    def ColourWipe(self):
        animations.ColourWipe(ledStrip, (0,0,0), int(1000/len(ledStrip)))
    
    def Rainbow(self):
        animations.Rainbow(ledStrip, numOfLoops = 10)


#Default run program
if __name__ == '__main__':
    ledStrip = PiCont.LedSetup()
    threading.Thread(target = flaskThread).start()
    t = threading.Thread(target = animationThread)
    t.start()
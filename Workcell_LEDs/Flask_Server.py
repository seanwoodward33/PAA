# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 15:03:32 2019

@author: sean_woodward
"""
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

#Define classes for functions
class Rainbow(Resource):
    def get(self):
        animations.Rainbow(ledStrip)

class Pixelwipe(Resource):
    def get(self):
        animations.PixelWipe(ledStrip,(255,0,255))

class Shutdown(Resource):
    def get(self):
        animations.ColourWipe(ledStrip, (0,0,0), int(1000/len(ledStrip)))
        
#Add functions to web address
api.add_resource(Rainbow, '/rainbow')
api.add_resource(Pixelwipe, '/pixelwipe')
api.add_resource(Shutdown, '/shutdown')


#Default run program
if __name__ == '__main__':
    ledStrip = PiCont.LedSetup()
    app.run(port = '5002')
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:06:26 2019

@author: Sean_Woodward
"""

import colorsys
import numpy as np

"""Functions to control LEDs"""
#Non-normalised HSV to RGB function
def HsvToRgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

#Run complete - Run rainbow animation
def RunComplete(self, section):
    self.ledArray[section[0]:section[1]][:,3] = 1
    ledCount = len(self.ledArray[section[0]:section[1]])
    #print(ledCount)
    if self.firstRun == True:
        for i in range(ledCount):
            for j in range(3):
                self.ledArray[section[0] + i][j] = HsvToRgb((((i)%(ledCount))/(ledCount)),1.0,1.0)[j]
    
    if self.firstRun == False:
        print (self.ledArray[section[0]][0:3])
        print (self.ledArray[section[0]+1][0:3])
        print (self.ledArray[section[0]+2][0:3])
        print (self.ledArray[section[0]+3][0:3])
        print(self.ledArray[section[0]:section[1]][:,0:3])
        print(np.roll(self.ledArray[section[0]:section[1]][:,0:3],1, axis = 0))
        self.ledArray[section[0]:section[1]][:,3] = np.roll(self.ledArray[section[0]:section[1]][:,3],1, axis = 0)
        print (self.ledArray[section[0]][0:3])
        print (self.ledArray[section[0]+1][0:3])
        print (self.ledArray[section[0]+2][0:3])
        print (self.ledArray[section[0]+3][0:3])
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:06:26 2019

@author: Sean_Woodward
"""

import colorsys

"""Functions to control LEDs"""
#Non-normalised HSV to RGB function
def HsvToRgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

#Run complete - Run rainbow animation
def RunComplete(self, section):
    self.ledArray[section[0],section[1]+1][:,3] = 1
    ledCount = len(self.ledArray[section[0],section[1]+1])+1
    if self.firstRun == True:
        while self.animationRun == True:
            for i in range(ledCount):
                for j in range(3):
                    self.ledArray[section[0] + i][j] = HsvToRgb((((i)%ledCount)/ledCount),1.0,1.0)[j]
    
    if self.firstRun == False:
        while self.animationRun == True:
            for i in range(ledCount):
                if self.animationRun == False: break
                self.ledArray[section[0] + i][0:3] = self.ledArray[section[0] + i - 1][0:3]
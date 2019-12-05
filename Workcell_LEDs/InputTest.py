# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:01:17 2019

@author: Sean_Woodward

Script to test GPIO inputs
"""
#Import relavent libraries
import board
import digitalio
import time

#Setup input
button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN

#run while loop to test
while True:
    if button.value == 1:
        print ("high value received")
        print ("button value equals: " + str(button.value))
        time.sleep(0.5)
        print ("0.5 seconds waited")
        time.sleep(0.5)
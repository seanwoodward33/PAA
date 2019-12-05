# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:01:17 2019

@author: Sean_Woodward
"""

import board
import digitalio
import time

button = digitalio.DigitalInOut(board.D4)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

while True:
    if button.value == 1:
        print ("high value received")
        time.sleep(0.5)
        print ("0.5 seconds waited")
        time.sleep(0.5)
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:16:21 2019

@author: Sean_Woodward
"""
#Import libraries
import board
import digitalio
import logging

#Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(asctime)s - (%(threadName)-10s) %(message)s')

#Setup inputs for Estops
Estop1 = digitalio.DigitalInOut(board.D2)
Estop2 = digitalio.DigitalInOut(board.D3)
Estop3 = digitalio.DigitalInOut(board.D4)


Estop1.direction = digitalio.Direction.INPUT
Estop2.direction = digitalio.Direction.INPUT
Estop3.direction = digitalio.Direction.INPUT


Estop1.pull = digitalio.Pull.DOWN
Estop2.pull = digitalio.Pull.DOWN
Estop3.pull = digitalio.Pull.DOWN

#Setup inputs for doors
Door1 = digitalio.DigitalInOut(board.D5)
Door2 = digitalio.DigitalInOut(board.D6)
Door3 = digitalio.DigitalInOut(board.D7)
Door4 = digitalio.DigitalInOut(board.D8)
Door5 = digitalio.DigitalInOut(board.D9)
Door6 = digitalio.DigitalInOut(board.D10)


Door1.direction = digitalio.Direction.INPUT
Door2.direction = digitalio.Direction.INPUT
Door3.direction = digitalio.Direction.INPUT
Door4.direction = digitalio.Direction.INPUT
Door5.direction = digitalio.Direction.INPUT
Door6.direction = digitalio.Direction.INPUT


Door1.pull = digitalio.Pull.DOWN
Door2.pull = digitalio.Pull.DOWN
Door3.pull = digitalio.Pull.DOWN
Door4.pull = digitalio.Pull.DOWN
Door5.pull = digitalio.Pull.DOWN
Door6.pull = digitalio.Pull.DOWN

#Setup array for reading input values
estopInputs = [0,0,0]
lastEstopInput = [0,0,0]
doorInputs = [0,0,0,0,0,0]
lastDoorInputs = [0,0,0,0,0,0]

while True:
    estopInputs[0] = Estop1.value
    estopInputs[1] = Estop2.value
    estopInputs[2] = Estop3.value
    doorInputs[0] = Door1.value
    doorInputs[1] = Door2.value
    doorInputs[2] = Door3.value
    doorInputs[3] = Door4.value
    doorInputs[4] = Door5.value
    doorInputs[5] = Door6.value
    
    for i in range(len(estopInputs)):
        if estopInputs[i] != lastEstopInput[i]:
            if lastEstopInput[i] = 1:
                    
            if inputs[i] = 0:
                pass
    
    lastInput = inputs
#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

T = 1.0/1000
out = True 
timerold = 0.0
timer = 0.0
try:
    while(True):
        timer = time.time()
        if timer - timerold >= T:
            GPIO.output(11, out)
            out = not out
            timerold = timer
        time.sleep(0.0001)        
except KeyboardInterrupt:
    GPIO.cleanup()

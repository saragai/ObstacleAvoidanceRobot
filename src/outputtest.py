#!/usr/bin/python
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)

count = 0
while count < 64:
    flag1 = False
    flag2 = False
    if count % 2:
        flag2 = True
    if count % 4 >= 2:
        flag1 = True
    
    GPIO.output(8, flag1)
    GPIO.output(10, flag2)
    count += 1
    time.sleep(0.25)

GPIO.cleanup()

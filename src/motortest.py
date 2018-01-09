#!/usr/bin/python3
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
AIN1 = 19
AIN2 = 26
freq = 1

GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)

GPIO.output(AIN1, True)
GPIO.output(AIN2, False)
time.sleep(1.0)
#pAIN1 = GPIO.PWM(AIN1, freq)
#pAIN2 = GPIO.PWM(AIN2, freq)

#pAIN1.start(0)
#pAIN2.start(0)

try:
    while True:
        for dc in range(100):
            GPIO.output(AIN2, True)
            #pAIN1.ChangeDutyCycle(50)
            time.sleep(1)
            #pAIN1.ChangeDutyCycle(80)
            GPIO.output(AIN2, False)
            time.sleep(1)
except KeyboardInterrupt:
    #pAIN1.stop()
    #pAIN2.stop()
    GPIO.cleanup()

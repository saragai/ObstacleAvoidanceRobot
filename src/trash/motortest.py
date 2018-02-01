#!/usr/bin/python
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
MODE = 5
AIN1 = 6
AIN2 = 13
BIN1 = 19
BIN2 = 26

GPIO.setup(MODE, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

GPIO.output(MODE, False)

def motor(a):
    GPIO.output(AIN1, a[0])
    GPIO.output(AIN2, a[1])
    GPIO.output(BIN1, a[2])
    GPIO.output(BIN2, a[3])


if __name__ == "__main__":
    try:
        while True:
            motor([1,0,0,1])
            time.sleep(1)
            motor([0,0,0,0])
            time.sleep(1)
            motor([0,1,1,0])
            time.sleep(1)
            motor([0,0,0,0])
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()

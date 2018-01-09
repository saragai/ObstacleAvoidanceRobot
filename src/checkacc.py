#!/usr/bin/python

from acctest import *
from motortest import motor
import time
import RPi.GPIO as GPIO

def minus(a,b):
    c = [a[i] - b[i] for i in range(len(a))]
    return c

if __name__ == "__main__":
    try:
        accinit = get_accel_data_lsb()
        count = 0
        while True:
            print(minus(get_accel_data_lsb(), accinit))
            time.sleep(0.01)
            count += 1
            if count == 100:
                print("\n=====change forward=====")
                motor([1,0,0,1])
            elif count == 200:
                print("\n=====change neutral=====")
                motor([0,0,0,0])
            elif count == 300:
                print("\n=====change backward=====")
                motor([0,1,1,0])
            elif count == 400:
                print("\n=====change neutral=====")
                motor([0,0,0,0])
                count = 0
                
    except KeyboardInterrupt:
        GPIO.cleanup()

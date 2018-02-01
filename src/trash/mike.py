#!/usr/bin/python3
import RPi.GPIO as GPIO
import concurrent.futures
from adcread import fft


ch = [0,1]
pool = concurrent.futures.ProcessPoolExecutor(max_workers=2)
result = list(pool.map(fft, ch))

try:
    while(True):
        for i in range(2):
            for j in result[i]:
                s = "-" * (int)(j)
                print(s)
            print("==========")
except KeyboardInterrupt:
    GPIO.cleanup()
"""
jobs = [adcread(0), adcread(1)]

for j in jobs:
    print(j.start())

for j in jobs:
    print(j.join())
"""

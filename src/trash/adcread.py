#!/usr/bin/python3
import multiprocessing
import numpy as np
#import serial
#import sys
import time
import RPi.GPIO as GPIO

SPI_SCLK = 11
SPI_MISO = 9
SPI_MOSI = 10
SPI_CE = 8

GPIO.setmode(GPIO.BCM)
GPIO.setup(SPI_SCLK, GPIO.OUT)
GPIO.setup(SPI_MOSI, GPIO.OUT)
GPIO.setup(SPI_MISO, GPIO.IN)
GPIO.setup(SPI_CE, GPIO.OUT)

def adcread(ch):
    GPIO.output(SPI_CE, GPIO.HIGH)
    GPIO.output(SPI_SCLK, GPIO.LOW)
    #build control bit (5bit)
    #   start bit(1) + single-ended(1) + channel(3bit)
    cmd = 0x18 | (ch & 0x07)
    GPIO.output(SPI_CE, GPIO.LOW)

    #send control bit
    for i in range(5):
        if cmd & 0x10:
            GPIO.output(SPI_MOSI, GPIO.HIGH)
        else:
            GPIO.output(SPI_MOSI, GPIO.LOW)
        cmd <<= 1
        GPIO.output(SPI_SCLK, GPIO.HIGH)
        GPIO.output(SPI_SCLK, GPIO.LOW)

    #recieve data
    dataval = 0
    for i in range(13): #null bit(1bit) + data(12bit)
        GPIO.output(SPI_SCLK, GPIO.HIGH)
        GPIO.output(SPI_SCLK, GPIO.LOW)
        if i == 0:
            continue    #skip null bit
        dataval <<= 1
        if GPIO.input(SPI_MISO) == GPIO.HIGH:
            dataval |= 0x01

    GPIO.output(SPI_CE, GPIO.HIGH)  #end communication
    return dataval 

def fft(ch):
    timer = time.time()
    n=512
    win = np.hamming(n)
    x = np.zeros(n)
    for i in range(n):
        x[i] = adcread(ch)
        time.sleep(0.0001)
    x = x - np.mean(x)
    X = np.fft.fft((x / np.max(x)) * win)
    #print(time.time() - timer)
    return np.abs(X[:n/2])

if __name__ == "__main__":
    try:
        print("ch0\n",fft(0))
        print("ch1\n",fft(1))
        #time.sleep(3)
        
        while(True):
            x1 = fft(1)
            x0 = fft(0)
            print("x0:{},\t{}".format(np.argmax(x0), np.max(x0)))
            print("x1:{},\t{}".format(np.argmax(x1), np.max(x1)))
            #time.sleep(0.5)    

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()


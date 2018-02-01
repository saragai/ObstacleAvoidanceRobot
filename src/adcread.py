#!/usr/bin/python3
import multiprocessing as mp
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
    #timer = time.time()
    n=512
    win = np.hamming(n)
    x = np.zeros(n)
    for i in range(n):
        x[i] = adcread(ch)
        time.sleep(0.0001)
    #print(x)
    x = x - np.mean(x)
    X = np.fft.fft((x / 2048) * win)
    #print(time.time() - timer)
    return np.abs(X[:n/2])

def fft2():
    n=512
    win = np.hamming(n)
    x0 = np.zeros(n)
    x1 = np.zeros(n)
    for i in range(n):
        x0[i] = adcread(0)
        x1[i] = adcread(1)
        time.sleep(0.0001)
    X0 = np.fft.fft(((x0 / 2048) - 1.0) * win)
    X1 = np.fft.fft(((x1 / 2048) - 1.0) * win)
    return np.abs(X0[:n/2]), np.abs(X1[:n/2])

def fft_multi():
    ret0 = None
    ret1 = None
    with mp.Pool(processes=10) as pool:
        ch0 = pool.apply_async(fft, (0, ))
        ch1 = pool.apply_async(fft, (1, ))
        ret0 = ch0.get()
        ret1 = ch1.get()
    return ret0, ret1

if __name__ == "__main__":
    mp.set_start_method('spawn')
    try:
        ch0, ch1 = fft2()
        print("fft_multi\n  ch0:{}\n  ch1:{}".format(ch0, ch1))
        """
        print("ch0\n",fft(0))
        print("ch1\n",fft(1))
        
        print("fft1")
        _ = fft(0)
        print("fft2")
        _ = fft(3)
        """

        time.sleep(2)
        
        while(True):
            x0, x1 = fft2()
            print("x0:{},\t{}".format(np.argmax(x0), np.max(x0)))
            print("x1:{},\t{}".format(np.argmax(x1), np.max(x1)))
            #time.sleep(0.5)    

    except KeyboardInterrupt:
        pass

    GPIO.cleanup()


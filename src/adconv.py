import numpy as np
import serial
import sys
import time
import matplotlib
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

SPI_SCLK = 11
SPI_MISO = 9
SPI_MOSI = 10
SPI_CE = 8

def readadc(ch):
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


def update(x):
    plt.cla()

    X = np.fft.fft(x)
    #freq = np.fft.fftfreq(x.shape[-1])
    freq = np.arange(x.shape[-1])
    plt.subplot(211)
    plt.plot(freq, np.abs(X))
    plt.subplot(212)
    plt.plot(freq, np.degrees(np.angle(X)))
    plt.show()

GPIO.setmode(GPIO.BCM)
GPIO.setup(SPI_SCLK, GPIO.OUT)
GPIO.setup(SPI_MOSI, GPIO.OUT)
GPIO.setup(SPI_MISO, GPIO.IN)
GPIO.setup(SPI_CE, GPIO.OUT)

lastval=0
fs = 1000
count = 0
val = 0
x = np.zeros(fs)

try:
    while True:
        val = readadc(0)
        
        if count == fs:
            count = 0
            x = x/4096
            update(x)
            print(val)
        x[count] = val
        count += 1

        # """
        #s = "*" * (int)(val/200)
        #print(s)
        time.sleep(1/fs)
        
except KeyboardInterrupt:
    pass

GPIO.cleanup()


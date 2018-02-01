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
    humm = np.hamming(x.shape[-1])
    
    X = np.fft.fft(x)
    Xwin = np.fft.fft(x*humm)
    #freq = np.fft.fftfreq(x.shape[-1])
    freq = np.linspace(0, x.shape[-1],x.shape[-1])
    plt.subplot(311)
    plt.plot(freq, np.abs(X))
    plt.subplot(312)
    plt.plot(freq, np.abs(Xwin))
    plt.subplot(313)
    plt.plot(freq, np.degrees(np.angle(X)))

GPIO.setmode(GPIO.BCM)
GPIO.setup(SPI_SCLK, GPIO.OUT)
GPIO.setup(SPI_MOSI, GPIO.OUT)
GPIO.setup(SPI_MISO, GPIO.IN)
GPIO.setup(SPI_CE, GPIO.OUT)


import matplotlib.animation as anm
fig = plt.figure(figsize = (10, 6))
def anime(i):
    
    plt.cla()

    lastval=0
    fs = 10000
    count = 0
    val = 0
    sample = 1000
    x = np.zeros(sample)
    t = time.time()
    try:
        while True:
            val = readadc(0)
            
            if count == sample:
                count = 0
                #print(x)
                print(time.time() - t)
                x = x/3000 - 1
                update(x)
                return
            x[count] = val
            count += 1

            # """
            #s = "*" * (int)(val/200)
            #print(s)
            time.sleep(1/fs/2)
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        quit()
try:
    ani = anm.FuncAnimation(fig, anime, interval=100)
    plt.show()
except:
    GPIO.cleanup()

#!/usr/bin/python
import smbus
import time

DEVICE_BUS = 1
DEV_ADDR = 0x18
ACC_X = 0x00
ACC_Y = 0x02
ACC_Z = 0x04
bus = smbus.SMBus(DEVICE_BUS)

def read_byte(adr):
    return bus.read_byte_data(DEV_ADDR, adr)

def read_word(adr):
    high = bus.read_byte_data(DEV_ADDR, adr)
    low = bus.read_byte_data(DEV_ADDR, adr+1)
    val = (high << 8)+  low
    return val

def get_accel_data_lsb():
    x = read_word(ACC_X)
    y = read_word(ACC_Y)
    z = read_word(ACC_Z)
    return [x,y,z]

if __name__ == "__main__":
    while 1:
        print(get_accel_data_lsb())
        time.sleep(0.01)

#!/usr/bin/python

from mcp3208 import MCP3208
import time

adc = MCP3208()
timer = time.time()

for i in range(100000):
    for i in range(8):
        print('ADC[{}]: {:.2f}'.format(i, adc.read(i)))
    time.sleep(0.5)

print("100000times:", time.time()-timer)

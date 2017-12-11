#!/usr/bin/env python

#test for input
import RPi.GPIO as GPIO
import subprocess
import time

class _Getch:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import tty, sys, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)


while True:
    GPIO.output(11, True)
    time.sleep(0.001)
    GPIO.output(11, False)
    time.sleep(0.001)

GPIO.cleanup()

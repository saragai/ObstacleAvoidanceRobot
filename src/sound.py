#!/usr/bin/python3
import subprocess

procs = []
procs.append(subprocess.Popen(['sudo ./speaker.py'], shell=True))
procs.append(subprocess.Popen(['sudo ./mike.py'], shell=True))
for proc in procs:
    proc.communicate() 

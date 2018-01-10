#!/usr/bin/python
import numpy as np
import Network
import copy
import time

from adcread import fft_multi
from acc import get_accel_data_lsb
import RPi.GPIO as GPIO

class Agent:
    def __init__(self):
        self.s = None
        self.a = None
        self.QNN = Network.Network(512, 9, weight_init_std=0.01)
        self.actions = ((0,0,0,0), (0,0,0,1), (0,0,1,0),
                        (0,1,0,0), (0,1,0,1), (0,1,1,0),
                        (1,0,0,0), (1,0,0,1), (1,0,1,0))

        self.oldQNN = copy.deepcopy(QNN)

        # Hyper Param
        self.batch_size = 20
        self.learning_rate = 0.1
        self.gamma = 0.99
        self.epsilon = 0.1

        self.accel_init = np.array(get_accel_data_lsb())

    def state(self):
        # [TODO] Get Sensor value
        self.s = fft_multi()
        return self.s

    def act(self, s):
        # Greedy epsilon
        if np.random.rand() < self.epsilon:
            self.a = np.random.choice(self.actions)
            return np.random.choice(self.actions)
        Q = self.QNN.predict(s)
        a = np.argmax(Q)
        return actions[a]
        

    def update(self, s, a, new_s, r):
        
        #t = r + self.gamma * np.max(self.oldQNN.predict(new_s)) # [Modified] # [TODO] use old Q
        t = r + self.gamma * np.max(self.QNN.predict(new_s))
        Q = self.QNN.predict(s)
        Q[a] = t
        grad = QNN.gradient(s, Q)

        for key in  ("W1", "b1"):
            QNN.params[key] -= self.learning_rate * grad[key]
        #return self.QNN.predict(s)[a]

    def reward(self, t):
        n = int(t*100)
        r = 0
        for i in range(n):
            time.sleep(0.01)
            accel = np.array(get_accel_data_lsb())
            accel = np.sum(np.abs(accel - accel_init))
            if accel < 1000: 
                r += -1
            elif accel > 5000:
                r += -n

        if r == 0:
            r = 1
        return r

    def initialize(self):
        s = self.s

    def main(self):
        self.initialize()
        count = 0
        while True:
            s = self.s
            a = self.act(s)
            r = self.reward(0.1)
            new_s = self.state()
            self.update(s, a, new_s, r)

if __name__ == "__main__":
    import subprocess
    subprocess.Popen(['speaker-test -t sine f 1000'], shell=True)
    try:
        agent.main()

    except KeyboardInterrupt:
        GPIO.cleanup()

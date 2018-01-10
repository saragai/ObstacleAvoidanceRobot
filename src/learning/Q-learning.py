#!/usr/bin/python
import numpy as np
import Network
import copy
import time

from adcread import fft2
from acc import get_accel_data_lsb
from motor import motor
import RPi.GPIO as GPIO

class Agent:
    def __init__(self):
        self.s = None
        self.a = None
        self.actions = ((0,0,0,0), (0,0,0,1), (0,0,1,0),
                        (0,1,0,0), (0,1,0,1), (0,1,1,0),
                        (1,0,0,0), (1,0,0,1), (1,0,1,0))
        self.QNN = Network.Network(512, len(self.actions), weight_init_std=0.1)

        #self.oldQNN = copy.deepcopy(self.QNN)

        # Hyper Param
        self.rewardtime = 0.1
        self.learning_rate = 0.1
        self.gamma = 0.99
        self.epsilon = 0.01

        self.accel_init = np.array(get_accel_data_lsb())

    def state(self):
        # [TODO] Get Sensor value
        s1, s2 = fft2()
        self.s = np.r_[s1, s2]
        self.s.shape = [1, 512]
        return self.s

    def act(self, s):
        # Greedy epsilon
        if np.random.rand() < self.epsilon:
            self.a = np.random.randint(len(self.actions))
            return self.a
        Q = self.QNN.predict(s)
        self.a = np.argmax(Q)
        return self.a
        

    def update(self, s, a, new_s, r):
        
        #t = r + self.gamma * np.max(self.oldQNN.predict(new_s)) # [Modified] # [TODO] use old Q
        t = r + self.gamma * np.max(self.QNN.predict(new_s))
        Q = self.QNN.predict(s)
        Q[0,a] = t
        grad = self.QNN.gradient(s, Q)

        for key in  ("W1", "b1"):
            #print("{} : {}".format(key, grad[key].shape))
            self.QNN.params[key] -= self.learning_rate * grad[key]
        #return self.QNN.predict(s)[a]

    def reward(self, t):
        n = int(t*100)
        r = 0
        for i in range(n):
            time.sleep(0.01)
            accel = np.array(get_accel_data_lsb())
            accel = np.sum(np.abs(accel - self.accel_init))
            if accel < 1000: 
                r += -1
            elif accel > 5000:
                r += -10 * n

        if r >= -n/3:
            r = 10
        else:
            r = r / n
        return r

    def initialize(self):
        self.s = self.state()

    def main(self):
        self.initialize()
        count = 0
        while True:
            s = self.s
            a = self.act(s)
            motor(self.actions[a])
            time.sleep(0.05)
            r = self.reward(self.rewardtime)
            print("actions: {},rewards: {}".format(self.actions[a],r))
            new_s = self.state()
            self.update(s, a, new_s, r)

if __name__ == "__main__":
    agent = Agent()
    try:
        agent.main()

    except KeyboardInterrupt:
        GPIO.cleanup()

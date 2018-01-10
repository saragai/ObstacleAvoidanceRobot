#!/usr/bin/python3
from collections import OrderedDict
import mymath as my
import layer as my
import numpy as np

class Network:
    def __init__(self, input_size, output_size, weight_init_std = 0.01):
        self.params = {}
        self.params["W1"] = weight_init_std * np.random.randn(input_size, output_size)
        self.params["b1"] = np.zeros(output_size)

        self.layers = OrderedDict()
        self.layers["Affine"] = my.Affine(self.params["W1"], self.params['b1'])
        
        #self.lastLayer = my.SoftmaxWithLoss()
        
    def predict(self, s):
        x = np.copy(s)
        #print("s shape:", s.shape)
        for layer in self.layers.values():
            x = layer.forward(x)
        return x

    def loss(self, s, t):
        y = self.predict(s)
        return y - t
        #return self.lastLayer.forward(y, t)

    def gradient(self, x, t):
        dout = self.loss(x, t)
        #print("dout :", dout.shape)

        layers = list(self.layers.values())
        layers.reverse()
        for layer in layers:
            dout = layer.backward(dout)
        grads = {}
        grads["W1"] = self.layers["Affine"].dW
        grads["b1"] = self.layers["Affine"].db

        return grads


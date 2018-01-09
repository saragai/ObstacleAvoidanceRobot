import numpy as np
import Network
import copy
class Agent:
    def __init__(self):
        self.s = None
        self.QNN = Network.Network(256, 9, weight_init_std=0.01)
        self.actions = ((0,0,0,0), (0,0,0,1), (0,0,1,0),
                        (0,1,0,0), (0,1,0,1), (0,1,1,0),
                        (1,0,0,0), (1,0,0,1), (1,0,1,0))

        self.oldQNN = copy.deepcopy(QNN)

        # Hyper Param
        self.batch_size = 20
        self.learning_rate = 0.1
        self.gamma = 0.99
        self.epsilon = 0.1

    def state(self, s):
        # [TODO] Get Sensor value
        self.s = s

    def act(self, s):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)
        Q = self.QNN.predict(s)
        a = np.argmax(Q)
        return actions[a]
        

    def update(s, a, new_s, r):
        t = r + self.gamma * np.max(self.oldQNN.predict(new_s)) # [Modified] # [TODO] use old Q
        Q = self.QNN.predict(s)
        Q[a] = t
        grad = QNN.gradient(s, Q)

        for key in  ("W1", "b1"):
            QNN.params[key] -= self.learning_rate * grad[key]

        return self.QNN.predict(s)[a]

    def 

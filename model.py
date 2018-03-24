import random

GRID_DIM = (20,20)

class Model(object):
    """MODEL"""

    def __init__(self):
        def randomInitVal(): return random.uniform(-0.1,0.1)
        self.threshold = randomInitVal()
        self.weights = [[randomInitVal() for c in xrange(GRID_DIM[0])] for r in xrange(GRID_DIM[1])]
        self.eta = 0.3
        self.epoch = 0


    def train(self,samples):
        def activation(s):
            sum = 0.0
            for r in xrange(len(self.weights)):
                for c in xrange(len(self.weights)):
                    sum += self.weights[r][c] * s[r][c]
            return 1.0 if sum > self.threshold else 0.0

        for s in samples:
            output = activation(s)
            target = s[GRID_DIM[0] - 1][GRID_DIM[1]]
            error = (target - output)
            #Adjust weights
            for r in xrange(len(self.weights)):
                for c in xrange(len(self.weights)):
                    self.weights[r][c] += self.eta * error * s[r][c]
            #Adjust threshold
            self.threshold += self.eta * error * -1



        self.epoch +=1

    def renewVariables(self):
        def randomInitVal(): return random.uniform(-0.1,0.1)
        self.threshold = randomInitVal()
        self.weights = [[randomInitVal() for c in xrange(GRID_DIM[0])] for r in xrange(GRID_DIM[1])]
        self.eta = 0.3
        self.epoch = 0

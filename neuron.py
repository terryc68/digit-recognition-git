class Neuron(object):

    def __init__(self, weights,threshold):
        self.weights = weights
        self.threshold = threshold

    def predict(self, inputs):
        def getTotalInput(a1, a2):
            sum = 0
            for r in xrange(len(a1)):
                for c in xrange(len(a1)):
                    sum += a1[r][c] * a2[r][c]
            return sum
        total = getTotalInput(inputs,self.weights)
        return True if total - self.threshold > 0 else False

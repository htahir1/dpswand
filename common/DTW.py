from dtw import dtw
import numpy as np
import matplotlib.pyplot as plt


class DynamicTimeWarping:
    """A simple example class"""

    def __init__(self):
        self.dist = 0
        self.cost = []
        self.acc = []
        self.path = []

    def calculate_error(self, training_data, test_data):
        self.dist, self.cost, self.acc, self.path = dtw(training_data, test_data, dist=lambda x, y: np.linalg.norm(x - y, ord=1))
        return self.dist

    def make_plot(self):
        plt.imshow(self.acc.T, origin='lower', cmap=plt.cm.gray, interpolation='nearest')
        plt.plot(self.path[0], self.path[1], 'w')
        plt.xlim((-0.5, self.acc.shape[0]-0.5))
        plt.ylim((-0.5, self.acc.shape[1]-0.5))
        plt.show()
from fastdtw import fastdtw
import dtw
import numpy as np
import math

def euclidean0_1(vector1, vector2):
    '''calculate the euclidean distance, no numpy
    input: numpy.arrays or lists
    return: euclidean distance
    '''
    dist = [(a - b)**2 for a, b in zip(vector1, vector2)]
    dist = math.sqrt(sum(dist))
    return dist


class DynamicTimeWarping:
    def __init__(self):
        self.dist = 0
        self.cost = []
        self.path = []

    def calculate_error_fast_dtw(self, template, test_data):
        self.dist, self.path = fastdtw(template, test_data, dist=euclidean0_1)
        return self.dist

    def calculate_error_full_dtw(self, template, test_data):
        self.dist, self.cost, self.acc, self.path = dtw(template, test_data, dist=lambda x, y: np.linalg.norm(x - y, ord=1))
        return self.dist

    def make_plot(self):
        # fig = plt.figure(1)
        # ax = fig.add_subplot(111)
        # plot1 = plt.imshow(self.cost.T, origin='lower', cmap=plt.cm.gray, interpolation='nearest')
        # plot2 = plt.plot(self.path[0], self.path[1], 'w')
        # xlim = ax.set_xlim((-0.5, self.cost.shape[0] - 0.5))
        # ylim = ax.set_ylim((-0.5, self.cost.shape[1] - 0.5))
        # plt.show()
        pass
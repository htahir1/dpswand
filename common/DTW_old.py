from dtw import dtw
import numpy as np
import matplotlib.pyplot as plt
import scipy

training_path = 'E:/Hamza/Digital Product School/Harry Potter Wand Project/Data/Circle Gesture/Training' \
                '/noise_triangle_hamza.csv'

test_path = 'E:/Hamza/Digital Product School/Harry Potter Wand Project/Data/Circle Gesture/Training' \
                '/triangles_lefttoright_chris.csv'

noise_test_path = 'E:/Hamza/Digital Product School/Harry Potter Wand Project/Data/Circle Gesture/Test/' \
            '/NOISE.csv'

def read_data(file):
    with open(file) as f:
        samples = [sample.split(', ') for sample in f.readlines()]

    return np.array(samples, dtype=float)


def slidingWindow(sequence, winSize, step=1):
    """Returns a generator that will iterate through
    the defined chunks of input sequence.  Input sequence
    must be iterable."""

    # Verify the inputs
    try:
        it = iter(sequence)
    except TypeError:
        raise Exception("**ERROR** sequence must be iterable.")
    if not ((type(winSize) == type(0)) and (type(step) == type(0))):
        raise Exception("**ERROR** type(winSize) and type(step) must be int.")
    if step > winSize:
        raise Exception("**ERROR** step must not be larger than winSize.")
    if winSize > len(sequence):
        raise Exception("**ERROR** winSize must not be larger than sequence length.")

    # Pre-compute number of chunks to emit
    numOfChunks = ((len(sequence) - winSize) / step) + 1

    # Do the work
    for i in range(0, numOfChunks * step, step):
        yield sequence[i:i + winSize]
# def rolling_window(a, window):
#     collected = []
#     for i in range(0, a.shape[0] - window):
#         collected.append(a[i:i+window, 0:a.shape[1]])
#     return np.array(collected)

def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

training_datas = read_data(training_path)
training_datas = slidingWindow(training_datas, 100)

test_data = read_data(test_path)

# noise_test_data = read_data(noise_test_path)

# plt.plot(training_data)
# plt.plot(test_data)
# #plt.plot(noise_test_data)
#
# plt.show()


for training_data in training_datas:
    dist, cost, acc, path = dtw(training_data, test_data, dist=lambda x, y: np.linalg.norm(x - y, ord=1))
    print 'Minimum distance found:', dist

    plt.imshow(acc.T, origin='lower', cmap=plt.cm.gray, interpolation='nearest')
    plt.plot(path[0], path[1], 'w')
    # plt.xlim((-0.5, acc.shape[0]-0.5))
    # plt.ylim((-0.5, acc.shape[1]-0.5))
    # plt.show()

print "Done"


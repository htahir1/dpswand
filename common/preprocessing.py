import json
import urllib2
import numpy as np
from scipy import signal
from common.Helper import convert_gesture_raw_to_np

standard_length_size = 25


def sinc_interp(x, s, u):
    """
    Interpolates x, sampled at "s" instants
    Output y is sampled at "u" instants ("u" for "upsampled")

    """
    if len(x) != len(s):
        raise Exception, 'x and s must be the same length'

    # Find the period
    T = s[1] - s[0]

    transposed = np.transpose(np.tile(np.arange(len(s)), (len(u), 1))) * T

    sincM = np.tile(u, (len(s), 1)) - transposed
    y = np.dot(x, np.sinc(sincM / T))

    return y


def resample_data(samples):
    global over_count
    global under_count

    new_samples = samples

    if samples.shape[0] < standard_length_size:
        # npad = ((missing_values_length, 0), (0, 0))
        # new_samples = np.pad(samples, pad_width=npad, mode='mean')
        new_samples = signal.resample(samples, standard_length_size)

    elif samples.shape[0] > standard_length_size:
        # new_samples = np.delete(new_samples, [0], axis=0)
        first_order_diff = np.diff(samples)
        mean_square = (first_order_diff ** 2).mean(axis=1)
        missing_values_length = new_samples.shape[0] - standard_length_size
        ind = np.argpartition(mean_square, missing_values_length)[:missing_values_length]
        new_samples = np.delete(samples, ind, axis=0)
    return new_samples


def resample_all_data():
    json_list = json.loads(urllib2.urlopen("http://dpswand.appspot.com/gesture").read())
    count = 0
    total = 0
    new_samples = []

    for jsn in json_list:
        content = jsn["raw_data"]
        samples = convert_gesture_raw_to_np(content)
        total += samples.shape[0]
        count += 1

        new_samples.append(resample_data(samples))


    print "total length {}".format(total)
    print "number of samples {}".format(count)

    print "Average sample length {}".format(total/count)

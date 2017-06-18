import json
import urllib2
import numpy as np
from common.Helper import convert_gesture_raw_to_np

standard_length_size = 25


def resample_data(samples):
    global over_count
    global under_count

    new_samples = samples

    if samples.shape[0] < standard_length_size:
        missing_values_length = standard_length_size - samples.shape[0]
        npad = ((missing_values_length, 0), (0, 0))
        new_samples = np.pad(samples, pad_width=npad, mode='mean')

    elif samples.shape[0] > standard_length_size:
        while new_samples.shape[0] > standard_length_size:
            new_samples = np.delete(new_samples, [0], axis=0)

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

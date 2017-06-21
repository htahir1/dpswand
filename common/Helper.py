import numpy as np

standard_length_size = 25
# from scipy import signal


def resample_data(samples):
    global over_count
    global under_count

    new_samples = samples

    if samples.shape[0] < standard_length_size:
        # npad = ((missing_values_length, 0), (0, 0))
        # new_samples = np.pad(samples, pad_width=npad, mode='mean')
        # new_samples = signal.resample(samples, standard_length_size)
        pass

    elif samples.shape[0] > standard_length_size:
        # new_samples = np.delete(new_samples, [0], axis=0)
        first_order_diff = np.diff(samples)
        mean_square = (first_order_diff ** 2).mean(axis=1)
        missing_values_length = new_samples.shape[0] - standard_length_size
        ind = np.argpartition(mean_square, missing_values_length)[:missing_values_length]
        new_samples = np.delete(samples, ind, axis=0)
    return new_samples

def convert_gesture_raw_to_np(raw_data):
    raw_data = raw_data.replace('\r', "")
    samples = [sample.split(', ') for sample in raw_data.split('\n')]
    return resample_data(normalize_data(np.array(samples, dtype=float)))


def normalize_data(x):
    return (x - x.min(0)) / x.ptp(0)
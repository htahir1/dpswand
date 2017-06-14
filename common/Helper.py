import numpy as np


def convert_gesture_raw_to_np(raw_data):
    raw_data = raw_data.replace('\r', "")
    samples = [sample.split(', ') for sample in raw_data.split('\n')]
    return normalize_data(np.array(samples, dtype=float))


def normalize_data(x):
    return (x - x.min(0)) / x.ptp(0)
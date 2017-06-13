import numpy as np
import json

def convert_gesture_raw_to_np(raw_data):
    raw_data = raw_data.replace('\r', "")
    samples = [sample.split(', ') for sample in raw_data.split('\n')]

    return np.array(samples, dtype=float)


with open('raw_data.csv') as file:
        json_obj = json.loads(file.read())

circles = []
noise = []
print json_obj
for js in json_obj:
    if js['name'] == 'circle':
        raw = convert_gesture_raw_to_np(js['raw_data'])
        circles.append({"name" : "Circle", "raw_data" : raw})
    if js['name'] == 'noise':
        pass


for circle in circles:
    print circle
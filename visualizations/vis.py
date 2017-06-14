import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import urllib2
import json
from common.DTW import DynamicTimeWarping
from pylab import pcolor, colorbar, xticks, yticks
from numpy import arange

with open('data.csv', 'r') as content_file:
    content = content_file.read()


def normalize_data(x):
    return (x - x.min(0)) / x.ptp(0)


def vis_3d(X, Y, Z, label):
    fig = plt.figure()
    ax = Axes3D(fig)
    # Plot the surface.
    ax.plot(X, Y, Z, label=label)
    ax.legend()
    plt.show()


def plot_heat_map(matrix, x_labels, y_labels):
    pcolor(matrix)
    colorbar()
    xticks(arange(0.5, matrix.shape[1] + 0.5), x_labels, rotation=90)
    yticks(arange(0.5, matrix.shape[0] + 0.5), y_labels)
    plt.tick_params(axis='both', labelsize=9)
    plt.show()


def heat_maps():
    json_list = json.loads(urllib2.urlopen("http://dpswand.appspot.com/gesture").read())

    dtw = DynamicTimeWarping()

    gyro_dist_matrix = []
    acc_dist_matrix = []
    mag_dist_matrix = []
    roll_dist_matrix = []
    pitch_dist_matrix = []
    heading_dist_matrix = []
    total_dist_matrix = []
    orientation_dist_matrix = []
    x_labels = []
    y_labels = []

    counter = 0
    for jsn in json_list:
        content = jsn["raw_data"]
        raw_data = content.replace('\r', "")
        samples = [sample.split(', ') for sample in raw_data.split('\n')]
        samples = normalize_data(np.array(samples, dtype=float))
        gyro_data = samples[:, :3]
        acceleration_data = samples[:, 3:6]
        magnetometer_data = samples[:, 6:9]
        roll = samples[:, 9:10]
        pitch = samples[:, 10:11]
        heading = samples[:, 11:12]
        orientation_data = samples[:, 9:12]

        gyro_dist_vec = []
        acc_dist_vec = []
        mag_dist_vec = []
        roll_dist_vec = []
        pitch_dist_vec = []
        heading_dist_vec = []
        total_dist_vec = []
        orientation_dist_vec = []

        x_labels.append(jsn["name"])

        if jsn["name"] == "Circle" or jsn["name"] == "Test":
            y_labels.append(jsn["name"])
            for json2 in json_list:
                content = json2["raw_data"]
                raw_data = content.replace('\r', "")
                samples_2 = [sample.split(', ') for sample in raw_data.split('\n')]
                samples_2 = normalize_data(np.array(samples_2, dtype=float))
                gyro_data_2 = samples_2[:, :3]
                acceleration_data_2 = samples_2[:, 3:6]
                magnetometer_data_2 = samples_2[:, 6:9]
                roll_2 = samples_2[:, 9:10]
                pitch_2 = samples_2[:, 10:11]
                heading_2 = samples_2[:, 11:12]
                orientation_data_2 = samples_2[:, 9:12]

                gyro_dist_vec.append(dtw.calculate_error_full_dtw(gyro_data, gyro_data_2))
                acc_dist_vec.append(dtw.calculate_error_full_dtw(acceleration_data, acceleration_data_2))
                mag_dist_vec.append(dtw.calculate_error_full_dtw(magnetometer_data, magnetometer_data_2))
                # roll_dist_vec.append(dtw.calculate_error_full_dtw(roll, roll_2))
                # pitch_dist_vec.append(dtw.calculate_error_full_dtw(pitch, pitch_2))
                # heading_dist_vec.append(dtw.calculate_error_full_dtw(heading, heading_2))
                orientation_dist_vec.append(dtw.calculate_error_full_dtw(orientation_data, orientation_data_2))
                total_dist_vec.append(dtw.calculate_error_full_dtw(samples[:, :9], samples_2[:, :9]))

            if jsn["name"] == "Circle":
                print "Circle " + str(counter)
            elif jsn["name"] == "Test":
                print "Triangle " + str(counter)

            counter += 1
            gyro_dist_matrix.append(gyro_dist_vec)
            acc_dist_matrix.append(acc_dist_vec)
            mag_dist_matrix.append(mag_dist_vec)
            roll_dist_matrix.append(roll_dist_vec)
            pitch_dist_matrix.append(pitch_dist_vec)
            heading_dist_matrix.append(heading_dist_vec)
            total_dist_matrix.append(total_dist_vec)
            orientation_dist_matrix.append(orientation_dist_vec)

    gyro_dist_matrix = np.array(gyro_dist_matrix)
    acc_dist_matrix = np.array(acc_dist_matrix)
    mag_dist_matrix = np.array(mag_dist_matrix)
    roll_dist_matrix = np.array(roll_dist_matrix)
    pitch_dist_matrix = np.array(pitch_dist_matrix)
    heading_dist_matrix = np.array(heading_dist_matrix)
    total_dist_matrix = np.array(total_dist_matrix)
    orientation_dist_matrix = np.array(orientation_dist_matrix)
    #
    # np.save("gyro_dist_matrix.dump", gyro_dist_matrix)
    # np.save("acc_dist_matrix.dump", acc_dist_matrix)
    # np.save("mag_dist_matrix.dump", mag_dist_matrix)
    # np.save("roll_dist_matrix.dump", roll_dist_matrix)
    # np.save("pitch_dist_matrix.dump", pitch_dist_matrix)
    # np.save("heading_dist_matrix.dump", heading_dist_matrix)
    # np.save("total_dist_matrix.dump", total_dist_matrix)

    # gyro_dist_matrix = np.load("gyro_dist_matrix.dump.npy")
    # mag_dist_matrix = np.load("mag_dist_matrix.dump.npy")
    # acc_dist_matrix = np.load("acc_dist_matrix.dump.npy")
    # total_dist_matrix = np.load("total_dist_matrix.dump.npy")
    # roll_dist_matrix = np.load("roll_dist_matrix.dump.npy")
    # pitch_dist_matrix = np.load("pitch_dist_matrix.dump.npy")
    # heading_dist_matrix = np.load("heading_dist_matrix.dump.npy")

    # pcolor(roll_dist_matrix)
    # colorbar()
    # xticks(arange(0.5, 40.5),range(0, 40))
    # yticks(arange(0.5, 20.5),range(0, 20))
    # plt.show()
    #
    plot_heat_map(acc_dist_matrix, x_labels, y_labels)
    plot_heat_map(mag_dist_matrix, x_labels, y_labels)
    plot_heat_map(gyro_dist_matrix, x_labels, y_labels)
    plot_heat_map(orientation_dist_matrix, x_labels, y_labels)
    plot_heat_map(total_dist_matrix, x_labels, y_labels)


def vis_3d_all():
    json_list = json.loads(urllib2.urlopen("http://dpswand.appspot.com/gesture").read())

    for jsn in json_list:
        content = jsn["raw_data"]
        raw_data = content.replace('\r', "")
        samples = [sample.split(', ') for sample in raw_data.split('\n')]
        samples = normalize_data(np.array(samples, dtype=float))
        gyro_data = samples[:, :3]
        acceleration_data = samples[:, 3:6]
        magnetometer_data = samples[:, 6:9]
        orientation_data = samples[:, 9:12]


        if jsn["name"] == "Test":
            X = gyro_data[:, :1].flatten()
            Y = gyro_data[:, 1:2].flatten()
            Z = gyro_data[:, 2:3].flatten()
            vis_3d(X, Y, Z, "Gyro" + jsn["name"])

            X = orientation_data[:, :1].flatten()
            Y = orientation_data[:, 1:2].flatten()
            Z = orientation_data[:, 2:3].flatten()
            vis_3d(X, Y, Z, "Orientation" + jsn["name"])

            X = acceleration_data[:, :1].flatten()
            Y = acceleration_data[:, 1:2].flatten()
            Z = acceleration_data[:, 2:3].flatten()
            vis_3d(X, Y, Z, "Acc" + jsn["name"])

            X = magnetometer_data[:, :1].flatten()
            Y = magnetometer_data[:, 1:2].flatten()
            Z = magnetometer_data[:, 2:3].flatten()
            vis_3d(X, Y, Z, "Mag" + jsn["name"])


vis_3d_all()
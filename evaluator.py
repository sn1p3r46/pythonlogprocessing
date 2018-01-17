import numpy as np


cutpoints = {

    3: [-np.inf, -0.43, 0.43, np.inf],
    4: [-np.inf, -0.67, 0, 0.67, np.inf],
    5: [-np.inf, -0.84, -0.25, 0.25, 0.84, np.inf],
    6: [-np.inf, -0.97, -0.43, 0, 0.43, 0.97, np.inf],
    7: [-np.inf, -1.07, -0.57, -0.18, 0.18, 0.57, 1.07, np.inf],
    8: [-np.inf, -1.15, -0.67, -0.32, 0, 0.32, 0.67, 1.15, np.inf],
    9: [-np.inf, -1.22, -0.76, -0.43, -0.14, 0.14, 0.43, 0.76, 1.22, np.inf],
    10: [-np.inf, -1.28, -0.84, -0.52, -0.25, 0, 0.25, 0.52, 0.84, 1.28,
         np.inf]

}


def standardize(x, mean, std):
    return (x - mean)/std


def evaluate(val, number_of_intervals):
    for i in range(len(cutpoints[number_of_intervals])):
        if val < cutpoints[number_of_intervals][i]:
            return i

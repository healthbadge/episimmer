import copy

import numpy as np


def average(tdict, number):
    avg_dict = copy.deepcopy(tdict)
    for k in avg_dict.keys():
        l = avg_dict[k]
        for i in range(len(l)):
            avg_dict[k][i] /= number
    return avg_dict


def stddev(tdict, t2_dict, number):
    stddev_dict = copy.deepcopy(tdict)
    for k in stddev_dict.keys():
        l = stddev_dict[k]
        for i in range(len(l)):
            stddev_dict[k][i] = np.sqrt(t2_dict[k][i] / number -
                                        (tdict[k][i] / number)**2)
    return stddev_dict

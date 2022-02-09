import copy
from typing import Dict, List

import numpy as np


def deep_copy_average(tdict: Dict[str, List[int]],
                      number: int) -> Dict[str, List[float]]:
    """
    This function returns the average of the values in the epidemic trajectory

    Args:
        tdict: Time series dictionary.
        number: Number of worlds

    Returns:
        Average of epidemic trajectory
    """
    avg_dict = copy.deepcopy(tdict)
    for k in avg_dict.keys():
        epidemic_trajectory_list = avg_dict[k]
        for i in range(len(epidemic_trajectory_list)):
            avg_dict[k][i] /= number
    return avg_dict


def deep_copy_stddev(tdict: Dict[str, List[int]], t2_dict: Dict[str,
                                                                List[int]],
                     number: int) -> Dict[str, List[float]]:
    """
    This function returns the standard deviation of the values in the epidemic trajectory.

    Args:
        tdict: Time series dictionary.
        t2_dict: Squared time series dictionary.
        number: Number of worlds

    Returns:
        Standard Deviation of epidemic trajectory
    """
    stddev_dict = copy.deepcopy(tdict)
    for k in stddev_dict.keys():
        epidemic_trajectory_list = stddev_dict[k]
        for i in range(len(epidemic_trajectory_list)):
            stddev_dict[k][i] = np.sqrt(t2_dict[k][i] / number -
                                        (tdict[k][i] / number)**2)
    return stddev_dict

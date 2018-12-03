"""
Application 3
"""

import random
import time

import matplotlib.pyplot as plt

import ALG_Closest_Pairs_and_Clustering as my_method
import alg_cluster


def gen_random_clusters(num_clusters):
    """
    :param num_clusters: cluster numbers
    :return: a list of clusters which is in the square with corners (+1/-1,+1/-1)
    """
    cluster_list = []
    for _ in range(num_clusters):
        new_cluster = alg_cluster.Cluster(set([]), random.random() * 2 - 1, random.random() * 2 - 1, 0, 0)
        cluster_list.append(new_cluster)
    return cluster_list

def running_time_plot(size_range):
    """
    :param size_range: test clusters range
    computed the running times for fast_closest_pair(cluster_list)
    and slow_closest_pair(cluster_list)
    """
    x = []
    y_slow = []
    y_fast = []
    for size in range(size_range[0], size_range[1] + 1):
        x.append(size)
        test_cluster = gen_random_clusters(size)
        test_cluster.sort(key = lambda cluster: cluster.horiz_center())
        start = time.clock()
        my_method.slow_closest_pair(test_cluster)
        end_slow = time.clock()
        my_method.fast_closest_pair(test_cluster)
        end_fast = time.clock()
        y_slow.append(end_slow - start)
        y_fast.append(end_fast - end_slow)
    plt.plot(x, y_slow, '-b', label='slow_closest_pair')
    plt.plot(x, y_fast, '-r', label='fast_closest_pair')
    plt.legend(loc='upper right')
    plt.xlabel("Number of Initial Clusters")
    plt.ylabel("Running time in sec")
    plt.title("Running Time Test by Using time.clock() in Desktop Python2")
    plt.show()





# running_time_plot([2, 200])
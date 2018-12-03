"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import copy
import math

import matplotlib.pyplot as plt
import urllib2

import alg_cluster

# conditional imports
if DESKTOP:
    import ALG_Closest_Pairs_and_Clustering  as alg_project3_solution    # desktop project solution
    import alg_clusters_matplotlib
else:
    import user41_HIEOP4ld7Q_2 as alg_project3_solution   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(30)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

# DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
# DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
# DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
# DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
# DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"

DATA_3108_URL = "unifiedCancerData_3108.csv"
DATA_896_URL = "unifiedCancerData_896.csv"
DATA_290_URL = "unifiedCancerData_290.csv"
DATA_111_URL = "unifiedCancerData_111.csv"

def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    # data_file = urllib2.urlopen(data_url)
    with open(data_url, 'r') as data_file:
        data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])]
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering

    Note that method may return num_clusters or num_clusters + 1 final clusters
    """

    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters

    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)

    return cluster_list


#####################################################################
# Code to load cancer data, compute a clustering and
# visualize the results

def compute_distortion(cluster_list, data_table):
    """
    compute distortion
    """
    cluster_error = 0
    copy_list = copy.deepcopy(cluster_list)
    for cluster in copy_list:
        cluster_error += cluster.cluster_error(data_table)
    return cluster_error

def plot_distortion(data_url, size_range):
    """
    :return:
    """
    data_table = load_data_table(data_url)
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    hc_list = singleton_list
    x = []
    y_hc = []
    y_kmc = []
    # compute distortion of hierarchical_clustering in specific range
    # Note: use the hierarchical cluster of size n to compute the size n-1 and so on.
    for size in range(size_range[1], size_range[0] - 1, -1):
        print len(hc_list)
        hc_list = alg_project3_solution.hierarchical_clustering(hc_list, size)
        y_hc.append(compute_distortion(hc_list, data_table))
    y_hc.reverse() # reverse the hc_list
    print y_hc
    for size in range(size_range[0], size_range[1] + 1):
        x.append(size)
        kmc_list = alg_project3_solution.kmeans_clustering(singleton_list, size, 5)
        y_kmc.append(compute_distortion(kmc_list, data_table))
    title = data_url[-7: -4]
    plt.plot(x, y_hc, '-b', label='hierarchical_clustering')
    plt.plot(x, y_kmc, '-r', label='k-means_clustering')
    plt.legend(loc='upper right')
    plt.xlabel("Number of Output Clusters")
    plt.ylabel("Distortion")
    plt.title(title + " county data sets")
    plt.show()


def run_example():
    """
    Load a data table, compute a list of clusters and
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA_896_URL)
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))

    # cluster_list = sequential_clustering(singleton_list, 15)
    # print "Displaying", len(cluster_list), "sequential clusters"

    cluster_list = alg_project3_solution.hierarchical_clustering(singleton_list, 9)
    print "Displaying", len(cluster_list), "hierarchical clusters"

    # cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, 9, 5)
    # print "Displaying", len(cluster_list), "k-means clusters"

    # calculate cluster_error of hierarchical_clustering and kmeans_clustering
    hc_error = compute_distortion(alg_project3_solution.hierarchical_clustering(singleton_list, 9), data_table)
    kmc_error = compute_distortion(alg_project3_solution.kmeans_clustering(singleton_list, 9, 5), data_table)
    print "cluster_error:\nhierarchical_clustring: ",hc_error,"\nkmeans_clustering: ",kmc_error

    # draw the clusters using matplotlib or simplegui
    if DESKTOP:
        # alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, False)
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)  #add cluster centers
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   # use toggle in GUI to add cluster centers

run_example()
# plot_distortion(DATA_111_URL, [6, 20])
# plot_distortion(DATA_290_URL, [6, 20])
# plot_distortion(DATA_896_URL, [6, 20])
# print DATA_3108_URL



























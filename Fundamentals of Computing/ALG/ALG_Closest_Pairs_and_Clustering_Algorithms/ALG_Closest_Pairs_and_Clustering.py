"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import copy

import alg_cluster


######################################################
# Code for closest pairs of clusters
# Ref: https://class.coursera.org/algorithmicthink2-004/quiz/feedback?submission_id=275

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters

    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    closest_pair = ("inf", -1, -1)
    for idx1 in range(len(cluster_list) - 1):
        for idx2 in range(idx1+1, len(cluster_list)):
            if pair_distance(cluster_list, idx1, idx2)[0] < closest_pair[0]:
                closest_pair = pair_distance(cluster_list, idx1, idx2)
    return closest_pair

def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip

    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.
    """
    cluster_strip = [idx for idx in range(len(cluster_list)) if abs(cluster_list[idx].horiz_center() - horiz_center) < half_width]
    cluster_strip.sort(key = lambda idx: cluster_list[idx].vert_center())
    strip_num = len(cluster_strip)
    closest_pair = (float('inf'), -1, -1)
    for idx1 in range(strip_num - 1):
        for idx2 in range(idx1 + 1, min([idx1 + 6, strip_num])):
            temp_pair = pair_distance(cluster_list, cluster_strip[idx1], cluster_strip[idx2])
            if temp_pair[0] < closest_pair[0]:
                closest_pair = temp_pair
    return tuple(closest_pair)

def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.
    """
    cluster_len = len(cluster_list)
    if cluster_len < 4:
        return slow_closest_pair(cluster_list)
    mid_idx = cluster_len / 2
    mid_horiz = (cluster_list[mid_idx - 1].horiz_center() + cluster_list[mid_idx].horiz_center()) / 2
    cluster_left = cluster_list[: mid_idx]
    cluster_right = cluster_list[mid_idx: ]
    closest_left = fast_closest_pair(cluster_left)
    closest_right = fast_closest_pair(cluster_right)
    closest_right = (closest_right[0], closest_right[1] + mid_idx, closest_right[2] + mid_idx)
#    closest_pair = max([closest_left, closest_right], key = lambda cluster: cluster[0])
    if closest_left[0] < closest_right[0]:
        closest_pair = closest_left
    else:
        closest_pair = closest_right
    closest_in_strip = closest_pair_strip(cluster_list, mid_horiz, closest_pair[0])
#    closest_pair = min([closest_pair, closest_in_strip], key = lambda cluster: cluster[0])
    if closest_in_strip[0] < closest_pair[0]:
        closest_pair = closest_in_strip
    return closest_pair


######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list

    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    new_cluster_list = copy.deepcopy(cluster_list)
    while len(new_cluster_list) > num_clusters:
        new_cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        cluster = fast_closest_pair(new_cluster_list)
        cluster2 = new_cluster_list.pop(cluster[2])
        new_cluster_list[cluster[1]].merge_clusters(cluster2)
    return new_cluster_list


######################################################################
# Code for k-means clustering


def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list

    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    old_cluster_list = [cluster for cluster in cluster_list]
    old_cluster_list.sort(key = lambda country:country.total_population())
    old_cluster_list = old_cluster_list[-num_clusters: ]
    for _ in range(num_iterations):
        new_cluster_list = [alg_cluster.Cluster(set([]), old_cluster.horiz_center(), old_cluster.vert_center(), 0, 0) for old_cluster in old_cluster_list]
        for cluster in cluster_list:
            # Find the old cluster center that is closest
            closest_idx = 0
            for old_idx in range(len(old_cluster_list)):
                if cluster.distance(old_cluster_list[old_idx]) < cluster.distance(old_cluster_list[closest_idx]):
                    closest_idx = old_idx
            new_cluster_list[closest_idx].merge_clusters(cluster)
        old_cluster_list = new_cluster_list
    return new_cluster_list


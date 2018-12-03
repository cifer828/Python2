"""
Project 2 - Connected components and graph resilience
"""
import collections
import random
import copy
import urllib2
import random
import time
import math
import matplotlib.pyplot as plt


############################################
# Provided code

# def copy_graph(graph):
#     """
#     Make a copy of a graph
#     """
#     new_graph = {}
#     for node in graph:
#         new_graph[node] = set(graph[node])
#     return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)

def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy.deepcopy(ugraph)

    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order

##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph

    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]

    print "Loaded graph with", len(graph_lines), "nodes"

    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

def bfs_visited(ugraph, start_node):
    """
    :param ugraph: an undirected graph
    :param start_node: start node
    :return: a set consisting of all nodes that are visited
    by a breadth-first search that starts at start_node
    https://d396qusza40orc.cloudfront.net/algorithmicthink/AT-Homework2/BFS-CC-Visited.jpg
    """
    queue = collections.deque()
    vistied = [start_node]
    queue.append(start_node)
    while len(queue) != 0:
        check_node = queue.popleft()
        for neighbor in ugraph[check_node]:
            if neighbor not in vistied:
                vistied.append(neighbor)
                queue.append(neighbor)
    return set(vistied)

def cc_visited(ugraph):
    """
    :param ugraph:  an undirected graph
    :return: a list of sets, where each set consists of all the nodes
    in a connected component
    https://d396qusza40orc.cloudfront.net/algorithmicthink/AT-Homework2/BFS-CC-Visited.jpg
    """
    remaining_nodes = copy.copy(ugraph)
    cc_set = []
    while len(remaining_nodes) != 0:
        idx = random.choice(remaining_nodes.keys())
        one_cc = bfs_visited(remaining_nodes, idx)
        cc_set.append(one_cc)
        for del_node in one_cc:
            del remaining_nodes[del_node]
    return cc_set

def largest_cc_size(ugraph):
    """
    Takes the undirected graph ugraph and returns the size (an integer)
    of the largest connected component
    """
    cc_lenths = [0]
    for temp_set in cc_visited(ugraph):
        cc_lenths.append(len(temp_set))
    return max(cc_lenths)

def compute_resilience(ugraph, attack_order):
    """
    :param ugraph: an undirected graph
    :param attack_order:  a list of nodes that will be attacked
    removed these nodes and their edges from the graph
    :return:a list whose (k+1)th entry is the size of the largest connected component in the graph
    after the removal of the first k nodes in attack_order
    """
    largest_cc_after = [largest_cc_size(ugraph)]
    copy_graph = copy.deepcopy(ugraph)   #use deepcopy not copy for child objects
    for attack_node in attack_order:
        for key in copy_graph.keys():
            if attack_node == key:
                del copy_graph[attack_node]
                break
        for value in copy_graph.values():
            if attack_node in value:
                value.remove(attack_node)
        int1 = largest_cc_size(copy_graph)
        largest_cc_after.append(int1)
        # print copy_graph
    return largest_cc_after

def ER_graph(nodes,probability):
    """
    :param nodes:  number of nodes
    :param probability: possiblily that two nodes have an egdge
    :return: an undirected graph
    """
    rand_graph = {}
    for node_num in range(nodes):
        rand_graph[node_num] = set([])
    for key in rand_graph.keys():
        for num in range(key + 1, nodes):
            randp = random.random()
            if randp < probability:
                rand_graph[key].add(num)
                rand_graph[num].add(key)

    return rand_graph

def make_complete_graph(num_nodes):
    """
    returns a dictionary corresponding
    to a complete directed graph
    """
    graph_dict = {}
    for edge_out in range(num_nodes):
        graph_dict[edge_out] =  set([])
        for edge_in in range(num_nodes):
            if edge_in != edge_out:
                graph_dict[edge_out].add(edge_in)

    return graph_dict

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm

    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities

    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a
        complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers

        Updates the list of node numbers so that each node number
        appears in correct ratio

        Returns:
        Set of nodes
        """

        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))

        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

    def generate(self, n):
        """
        generate UPA graph
        """
        m = self._num_nodes
        DPA_graph = make_complete_graph(m)
        for i in range(m ,n):
            neighbor = self.run_trial(m)
            DPA_graph[i] = neighbor
            for step in neighbor:
                DPA_graph[step].add(i)
        return DPA_graph

def random_order(graph):
    """
    :param graph: an undirected graph
    :return: a list of nodes in the graph in random order
    """
    temp_graph = copy.deepcopy(graph)
    all_nodes = temp_graph.keys()
    attack_order = []
    for _ in range(len(graph)):
        rand_pop = all_nodes.pop(random.randrange(len(all_nodes)))
        attack_order.append(rand_pop)
    return attack_order

def edge_nums(graph):
    """
    return number of edges of the graph
    """
    edge_num = 0
    for value in graph.values():
        edge_num += len(value)
    return edge_num / 2

def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting O(n^2)
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy.deepcopy(ugraph)
    order = []
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node

        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order

def fast_target_order(graph):
    """
    Compute a fast attack order consisting O(n)
    of nodes of maximal degree

    Returns:
    A list of nodes
    """
    new_graph = copy.deepcopy(graph)
    DegreeSets = {}
    for k in range(len(new_graph)):
        DegreeSets[k] = set([])
    for key in new_graph.keys():
        d = len(new_graph[key])
        DegreeSets[d].add(key)
    L = []
    for k in range(len(new_graph) - 1, -1, -1):
        while DegreeSets[k]:
            u = random.choice(list(DegreeSets[k]))
            DegreeSets[k].remove(u)
            for neighbor in new_graph[u]:
                d = len(new_graph[neighbor])
                DegreeSets[d].remove(neighbor)
                DegreeSets[d - 1].add(neighbor)
                new_graph[neighbor].remove(u)
            L.append(u)
            del new_graph[u]
    return L





EX_GRAPH1 = {0:set([1, 4, 6]), 1:set([0, 2, 6]), 2:set([1, 3, 6]), 3:set([2, 6]),
             4:set([0, 5]), 5:set([4]), 6:set([0, 1, 2, 3]), 7:set([])}

GRAPH2 = {1: set([2, 4, 6, 8]),
          2: set([1, 3, 5, 7]),
          3: set([2, 4, 6, 8]),
          4: set([1, 3, 5, 7]),
          5: set([2, 4, 6, 8]),
          6: set([1, 3, 5, 7]),
          7: set([2, 4, 6, 8]),
          8: set([1, 3, 5, 7])}

# print fast_target_order(GRAPH2)
# print cc_visited(EX_GRAPH1)
# print largest_cc_size(EX_GRAPH1)
# print compute_resilience(EX_GRAPH1, [0, 1])
# print compute_resilience(GRAPH2, [1, 3, 5, 7, 2, 4, 6, 8])
# print random_order(GRAPH2)

############################
#generate three graphs: computer network, ER, UPA
#Three graphs should have same number of nodes and approximately the same number of edges.

c = UPATrial(3)
UPAGraph = c.generate(1239)
computer_graph = load_graph(NETWORK_URL)
ERGraph = ER_graph(1239, 0.004)

print edge_nums(ERGraph)
print edge_nums(computer_graph)
print edge_nums(UPAGraph)

# def x_y(graph):
#     y = compute_resilience(graph, fast_target_order(graph))
#     # y = compute_resilience(graph, random_order(graph))
#     return y
#
# plt.plot(x_y(computer_graph), '-b', label='computer network')
# plt.plot(x_y(ERGraph), '-r', label='ERGraph p = 0.002')
# plt.plot(x_y(UPAGraph), '-y', label='UPAGraph m = 5')
# plt.xlim(0, 1239)
# plt.legend(loc='upper right')
# plt.xlabel("The number of nodes removed")
# plt.ylabel("The largest connect component")
# plt.title("Resilience of the network, ER and UPA graphs")
#
# plt.show()





#running time test

# def run_time(n):
#     c = UPATrial(5)
#     UPAGraph = c.generate(n)
#     targeted_order(UPAGraph)
#     targeted_time = time.clock()
#     fast_target_order(UPAGraph)
#     fast_time = time.clock() - targeted_time
#     return [targeted_time, fast_time]
# x = [i for i in range(10, 1000, 10)]
# y_target = [run_time(n)[0] for n in x]
# y_fast =  [run_time(n)[1] for n in x]
# print x
# print y_target
# print y_fast
# plt.plot(x, y_target, '-b', label='targeted_order')
# plt.plot(x, y_fast, '-r', label='fast_targeted_order')
# plt.legend(loc='upper right')
# plt.xlabel("Number of nodes")
# plt.ylabel("Running times")
# plt.title("Running Time Test by Using time.clock() in Python2")
# plt.show()
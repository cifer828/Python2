# coding=utf-8
"""
Project 1 Degree distributions for graphs
"""

#Three directed graphs
EX_GRAPH0 = {0:set([1, 2]), 1:set(), 2:set()}
EX_GRAPH1 = {0:set([1, 4, 5]), 1:set([2, 6]), 2:set([3]), 3:set([0]),
             4:set([1]), 5:set([2]), 6:set([])}
EX_GRAPH2 = {0:set([1, 4, 5]), 1:set([2, 6]), 2:set([3, 7]), 3:set([7]),
             4:set([1]), 5:set([2]), 6:set([]), 7:set([3]),
             8:set([1, 2]), 9:set([0, 3, 4, 5, 6, 7])}


"""
Provided code for Application portion of Module 1

Imports physics citation graph
"""

# general imports
import urllib2
import matplotlib.pyplot as plt
import random
from matplotlib.ticker import MultipleLocator, FormatStrFormatter


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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

def compute_in_degrees(digraph):
    """
    return a dict including the number of edges
    whose head matches a particular node
    """
    indegree_dict = {}
    for keys in digraph.keys():
        indegree_dict[keys] = 0
    for key in digraph.keys():
        for node in digraph[key]:
            indegree_dict[node] += 1
        print key
    return indegree_dict

def in_degree_distribution(digraph):
    """
    Return a dict: key = in-degrees of nodes
                 value = number of nodes with that in-degree
    In-degrees with no corresponding nodes in the graph
    are not included
    """
    in_degree_dict = compute_in_degrees(digraph)
    distribute_dict = {}
    for step in range(1, len(in_degree_dict)):
        distribute_dict[step] = 0
    for key in in_degree_dict.keys():
        index = in_degree_dict[key]
        if index != 0:
            distribute_dict[index] += 1
    for key in distribute_dict.keys():
        if distribute_dict[key] == 0:
            del distribute_dict[key]
        else:
            print key
    return distribute_dict

def norm_distribut(digraph):
    norm_dict = in_degree_distribution(digraph)
    total_edges = 0
    sum2one = 0
    step = 0
    for key in norm_dict.keys():
        step += 1
        total_edges += norm_dict[key]
    for key in norm_dict.keys():
        norm_dict[key] = float(norm_dict[key]) / total_edges
        sum2one += norm_dict[key]
    print "Sum of distribution = ",sum2one
    return norm_dict

def random_indegree(nodes,probability):
    rand_graph = {}
    for node_num in range(nodes):
        rand_graph[node_num] = set([])
    for key in rand_graph.keys():
        for num in range(nodes):
            if key != num:
                randp = random.random()
                if randp < probability:
                    rand_graph[key].add(num)
    return rand_graph

class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm

    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities

    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a
        complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]

    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers

        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities

        Returns:
        Set of nodes
        """

        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))

        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

    def generate(self, n):
        """
        generate DPA graph
        """
        m = self._num_nodes
        DPA_graph = make_complete_graph(m)
        for i in range(m ,n):
            temp_graph = self.run_trial(m)
            DPA_graph[i] = temp_graph
            # for step in temp_graph:
            #     DPA_graph[step].add(i)

        return DPA_graph

# Different graphs for testing

# test_graph = make_complete_graph(100)
# test_graph = random_indegree(27770, 0.0005)
# test_graph = load_graph(CITATION_URL)
# test_graph = EX_GRAPH2
c = DPATrial(4)
test_graph = c.generate(5)
print test_graph
# loglog plot
x = norm_distribut(test_graph).keys()
y = norm_distribut(test_graph).values()

plt.loglog(x,y,'o')
plt.xlabel("In-degree (log)")
plt.ylabel("Distribution (log)")
plt.title("In-degree distribution Plot for DPA graph")
plt.show()





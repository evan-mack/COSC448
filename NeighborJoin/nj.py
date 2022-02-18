import sys

import numpy as np
import networkx as nx
import pydot
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout


def q_matrix(dist):
    n = len(dist)

    # initialize the output matrix
    q = np.zeros_like(dist)

    # fill in the matrix
    for i in range(n):
        for j in range(n):
            if i != j:
                q[i][j] = (n - 2) * dist[i][j] - (np.sum(dist[i]) + np.sum(dist[j]))
    return q


def min_index(q):
    n = len(q)
    min_val = sys.maxsize
    for i in range(n):
        for j in range(i, n):
            if q[i][j] < min_val:
                min_val = q[i][j]
                min_idx = (i, j)
    return min_idx


# distance between the two closest unpaired points in the distance matrix. These are connected in a new node with
# calculated distances
def pair_distance(dist, ab):
    a, b = ab[0], ab[1]
    n = len(dist)
    delta_a = 0.5 * dist[a][b] + 1 / (2 * n - 4) * (np.sum(dist[a]) - np.sum(dist[b]))
    delta_b = dist[a][b] - delta_a

    return float(delta_a), float(delta_b)


# create new distance matrix with the distance of all unpaired points to newly created node
def dist_to_new_node(dist, min_idx):
    n = len(dist) - 1
    d = np.zeros((n, n))
    a, b = min_idx[0], min_idx[1]

    # copy non-new distances to matrix
    k = l = 1
    for i in range(n):
        if i == a or i == b:
            continue
        for j in range(n):
            if j == a or j == b:
                continue
            d[k][l] = dist[i][j]
            l += 1
        k += 1
        l = 1

    # calculate distance to newly created node to each other unpaired element
    m = 1
    for i in range(n):
        if i == a or i == b:
            continue
        d[0][m] = d[m][0] = 0.5 * (d[a][i] + d[b][i] - d[a][b])
        m += 1

    print(d)
    return d


def build_graph(dist, names):
    """
    Neighbor join algorithm proceeds as follows:
        1. Calculate the Q-matrix given the current distance matrix between all nodes
        2. Find the pair of distinct taxa (a, b) for which Q[a][b] is the minimum value. These taxa are joined to a new
           node.
        3. Calculate the distance from this new node to each taxa.
        4. Recalculate the distance matrix to each other taxa outside of the pair used to the new node.
        5. Repeat while replacing the pair of joined neighbors with the new node.

    In service of creating a displayable tree, the following process is followed to allow for creation of the binary
    tree structure:
        - add all starting nodes to an empty graph e.g., the list of names of organisms
        - iteratively follow the algorithm and generate newly created nodes and distances. Add each set to a master list
        - add the generated list to the graph and return the graph object for visualization
    """
    g = nx.Graph()
    g.add_nodes_from(names)

    while len(dist[0]) > 2:
        q = q_matrix(dist)
        min_idx = min_index(q)
        pair_dist = pair_distance(dist, min_idx)

        # use calculated information to update graph structure
        new_node_name = names[min_idx[0]] + names[min_idx[1]]
        g.add_node(new_node_name)
        new_edges = [(min_idx[0], new_node_name, {'weight': pair_dist[0]}), (min_idx[1], new_node_name, {'weight':pair_dist[1]})]
        g.add_edges_from(new_edges)

        # calculate the new distance matrix
        dist = dist_to_new_node(dist, min_idx)

    return g


def main():
    test_matrix = [[0, 5, 9, 9, 8],
                   [5, 0, 10, 10, 9],
                   [9, 10, 0, 8, 7],
                   [9, 10, 8, 0, 3],
                   [8, 9, 7, 3, 0]]
    g = build_graph(test_matrix, names=list('abcde'))
    pos = graphviz_layout(g, prog='dot')
    nx.draw(g, pos)
    plt.show()


main()
exit(0)
import math
import networkx as nx
import random


def calc_dist(graph, permutation):
    dis = 0
    for i in range(0, len(permutation)):
        dis = dis + graph[permutation[i]][permutation[(i + 1) % len(permutation)]]['weight']
    return dis


def inversion(permutation, i, j):
    while i < j:
        permutation[i], permutation[j] = permutation[j], permutation[i]
        i += 1
        j -= 1
    return permutation


def swap(permutation, i, j):
    permutation[i], permutation[j] = permutation[j], permutation[i]
    return permutation


def generate_graph(n, seed, type_of_problem):
    new_graph = nx.DiGraph()
    random.seed(10)

    if type_of_problem == "sym":

        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                weight = random.randrange(1, 1000)
                new_graph.add_edge(i, j % (n + 1), weight=weight)
                new_graph.add_edge(j, i % (n + 1), weight=weight)

    elif type_of_problem == "asym":

        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                new_graph.add_edge(i, j % (n + 1), weight=random.randrange(1, 1000))
                new_graph.add_edge(j, i % (n + 1), weight=random.randrange(1, 1000))

    elif type_of_problem == "full":

        tmp = nx.complete_graph(range(1, n + 1))

        for (node1, node2, data) in tmp.edges(data=True):
            tmp[node1][node2]['weight'] = random.randrange(1, 1000)

        return tmp

    else:

        node_list = []
        for i in range(1, n + 1):
            x = random.randrange(1, 1000)
            y = random.randrange(1, 1000)
            node_list.append((i, x, y))

        for out_edge in node_list:
            for to_edge in node_list:

                if out_edge == to_edge:
                    continue
                number = int(math.sqrt((out_edge[1] - to_edge[1]) ** 2 + (out_edge[2] - to_edge[2]) ** 2))
                new_graph.add_edge(out_edge[0], to_edge[0], weight=number)

    return new_graph

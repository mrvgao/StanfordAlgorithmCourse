"""
Implements the Random Contract Algorithm.
"""
from graph import Graph
import random
from copy import deepcopy
import numpy as np


def random_select_vertex(graph, num=1):
    vertices = graph.get_vertices()
    random.shuffle(vertices)
    if num == 1: return vertices[0]
    else: return vertices[:num]


def random_contract_one_pass(graph: Graph):
    while len(graph.get_vertices()) > 2:
        random_vertice_1, random_vertice_2 = random_select_vertex(graph, num=2)
        new_vertex = graph.merge_vertices([random_vertice_1, random_vertice_2])
        graph.remove_one_vertex_self_cycle(new_vertex)
    return graph


def random_contract(g: Graph, verboes=False):
    n = len(g.get_vertices())
    original_g = deepcopy(g)

    run_times = n * n * np.log(n)
    constant = 100
    run_times = int(constant * run_times)
    min_cuts = float('inf')
    for i in range(run_times):
        random.seed(i)
        tmp_g = random_contract_one_pass(original_g)
        cuts = len(tmp_g.adjacency[tmp_g.get_vertices()[0]])
        if cuts < min_cuts: min_cuts = cuts
        original_g = deepcopy(g)

        if verboes:
            print('{}/{} min-cuts: {}'.format(i+1, run_times, min_cuts))

    return min_cuts


if __name__ == '__main__':
    data = open('data/kargerMinCut.txt')
    nodes = []
    connections = []

    for ii, line in enumerate(data):
        vertices = line.strip().split('\t')
        nodes.append(vertices[0])
        connections += [(vertices[0], int(v)) for v in vertices[1:]]

    graph = Graph(nodes=nodes, connections=connections)
    min_cuts = random_contract(graph, verboes=True)
    print(min_cuts)


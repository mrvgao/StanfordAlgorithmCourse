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
    while len(list(filter(lambda v: len(graph.adjacency[v]) > 0, graph.get_vertices()))) > 2:
        random_vertex_1, random_vertex_2 = random_select_vertex(graph, num=2)
        while len(graph.adjacency[random_vertex_1]) == 0 or len(graph.adjacency[random_vertex_2]) == 0:
            random_vertex_1, random_vertex_2 = random_select_vertex(graph, num=2)
        new_vertex = graph.merge_vertices([random_vertex_1, random_vertex_2])
        graph.remove_one_vertex_self_cycle(new_vertex)
    return graph


def random_contract(g: Graph, verboes=False):
    n = len(g.get_vertices())
    original_g = deepcopy(g)

    run_times = n * n * np.log(n)
    constant = 1
    run_times = int(constant * run_times)
    min_cuts = float('inf')
    for i in range(run_times):
        random.seed(i)
        tmp_g = random_contract_one_pass(original_g)
        tmp_g_none_empty_vertices = list(filter(lambda v: len(g.adjacency[v]) > 0, tmp_g.get_vertices()))
        assert tmp_g_none_empty_vertices
        one_vertex, another_vertex = tmp_g_none_empty_vertices.get_vertices()
        assert tmp_g.adjacency[one_vertex][another_vertex] == tmp_g.adjacency[another_vertex][one_vertex]
        cuts = tmp_g.adjacency[one_vertex][another_vertex]
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
        nodes.append(int(vertices[0]))
        connections += [(int(vertices[0]), int(v)) for v in vertices[1:]]

    print('file load finish')
    graph = Graph(nodes=nodes, connections=connections)
    min_cuts = random_contract(graph, verboes=True)
    print(min_cuts)


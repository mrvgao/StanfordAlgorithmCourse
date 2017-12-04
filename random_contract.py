"""
Implements the Random Contract Algorithm.
"""
from graph import Graph
from random import Random
from copy import deepcopy
import numpy as np
import pickle
from multiprocessing import Pool
from multiprocessing import cpu_count


def random_select_vertex(graph, num=1, r=None):
    if r is None: random = Random()
    vertices = graph.get_vertices()
    random.shuffle(vertices)
    if num == 1: return vertices[0]
    else: return vertices[:num]


def random_contract_one_pass(graph: Graph, random=None):
    while len(list(filter(lambda v: len(graph.adjacency[v]) > 0, graph.get_vertices()))) > 2:
        random_vertex_1, random_vertex_2 = random_select_vertex(graph, num=2)
        while len(graph.adjacency[random_vertex_1]) == 0 or len(graph.adjacency[random_vertex_2]) == 0:
            random_vertex_1, random_vertex_2 = random_select_vertex(graph, num=2, random=random)
        new_vertex = graph.merge_vertices([random_vertex_1, random_vertex_2])
        graph.remove_one_vertex_self_cycle(new_vertex)
    return graph


def load_pickle(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)


def random_contract(graph : Graph, verboes=True, cpu=None):
    print(verboes)
    n = len(graph.adjacency)
    m = np.log(n)

    # graph_pickle_f = 'graph.pickle'
    # with open(graph_pickle_f, 'wb') as f:
    #     pickle.dump(graph, f)

    run_times = n * n * np.log(m)
    constant = 20
    run_times = int(constant * run_times)
    min_cuts = float('inf')
    for i in range(run_times):
        # graph = load_pickle(graph_pickle_f)
        original_graph = deepcopy(graph)
        random = Random(x=i)
        assert len(original_graph.get_vertices()) == 200, original_graph.get_vertices()
        tmp_g = random_contract_one_pass(original_graph, random=random)
        tmp_g_none_empty_vertices = list(filter(lambda v: len(tmp_g.adjacency[v]) > 0, tmp_g.get_vertices()))
        assert tmp_g_none_empty_vertices
        one_vertex, another_vertex = tmp_g_none_empty_vertices
        assert tmp_g.adjacency[one_vertex][another_vertex] == tmp_g.adjacency[another_vertex][one_vertex]
        cuts = tmp_g.adjacency[one_vertex][another_vertex]
        if cuts < min_cuts: min_cuts = cuts

        if verboes and i % 10 == 0:
            print('cpu: {} {}/{} cuts: {} min-cuts: {}'.format(cpu, i+1, run_times, cuts, min_cuts))

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
    # min_cross_cuts = random_contract(graph, verboes=True)
    cpu_number = cpu_count()
    print('cpu number is :{}'.format(cpu_number))
    pool = Pool(processes=cpu_count())  # number for cup_number is used.

    arguments = [(graph, True, i) for i in range(cpu_number)]
    results = pool.starmap(random_contract, arguments)

import random
import numpy as np
import copy


def random_select_vertices(graph):
    x = random.choice(list(graph.keys()))
    y = random.choice(graph[x])

    assert x in graph
    assert y in graph

    return x, y


def contract_graph(graph, x, y):
    graph[x] += graph[y]
    graph.pop(y)

    for v in graph:
        for i in range(len(graph[v])):
            if graph[v][i] == y:
                graph[v][i] = x

    graph[x] = [v for v in graph[x] if (v != y and v != x)]

    return graph


def random_contract_graph(graph):
    while len(graph) > 2:
        x, y = random_select_vertices(graph)
        graph = contract_graph(graph, x, y)

    return len(graph[list(graph.keys())[0]])


def random_n_pass(graph, seed=0):
    n = len(graph)
    mincuts = len(graph) * len(graph)
    random.seed(seed)
    for i in range(int(n * n * np.log(n))):
        original_graph = copy.deepcopy(graph)
        assert len(original_graph) == 200
        mincuts = min(random_contract_graph(original_graph), mincuts)
        print("{} {}".format(i, mincuts))

    return mincuts


if __name__ == '__main__':
    graph = {}

    with open('data/kargerMinCut.txt') as f:
        for line in f:
            numbers = list(map(int, line.strip().split()))
            graph[numbers.pop(0)] = numbers

    seed = 1
    random_n_pass(graph, seed)

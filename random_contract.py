"""
Implements the Random Contract Algorithm.
"""

import random


def get_graph_vertices(g): return list(g.keys())


def get_vertex_edges(g, vertex): return g[vertex]


def remove_self_cycle(g, n):
    if n not in g: return g

    vertices_cluster = n.strip().split()
    g[n] = list(filter(lambda x: x not in vertices_cluster, get_vertex_edges(g, n)))

    return g


def merge_two_vertices_edges(v1, v2):
    return v1 + v2


def delete_graph_node(g, v1):
    del g[v1]
    return g


def delete_graph_nodes(g, vertices):
    [delete_graph_node(g, v) for v in vertices]
    return g


def merge_two_vertices(v1, v2):
    n1_nodes = v1.strip().split('\t')
    n2_nodes = v2.strip().split('\t')
    new_vertex = " ".join(n1_nodes + n2_nodes)
    return new_vertex

# Graph API ends.


def merge_graph_nodes(g, n1, n2):
    new_node = merge_two_vertices(n1, n2)
    new_edge = merge_two_vertices_edges(get_vertex_edges(g, n1),
                                        get_vertex_edges(g, n2))
    g[new_node] = new_edge

    all_adjicent_vertices = get_vertex_edges(g, new_node)

    for v in all_adjicent_vertices:
        if v not in g: continue
        g[v] = list(filter(lambda x: x not in new_node.split(), g[v]))
        g[v].append(new_node)

    delete_graph_nodes(g, [n1, n2])

    return g


def random_contract_graph(g, dependancy_injection=None, verbose=False):
    while len(g) > 2:
        all_nodes = get_graph_vertices(g)

        if dependancy_injection:
            seed = next(dependancy_injection)
            random.seed(seed)

        random.shuffle(all_nodes)
        n1, n2 = all_nodes[:2]

        g = merge_graph_nodes(g, n1, n2)
        new_vertex = merge_two_vertices(n1, n2)
        if verbose: print('graph size: {}'.format(len(g)))
        g = remove_self_cycle(g, new_vertex)

    all_nodes = get_graph_vertices(g)
    assert len(all_nodes) == 2
    assert len(get_vertex_edges(g, all_nodes[0])) == len(get_vertex_edges(g, all_nodes[1])), g

    return g


def random_generator():
    L = [9, 1, 2]
    for i in L:
        yield i

if __name__ == '__main__':

    g = {'1': ['0', '1']}
    g = remove_self_cycle(g, '1')

    assert g['1'] == ['0']

    g = {'1': ['1', '0', '1']}
    g = remove_self_cycle(g, '1')

    assert g['1'] == ['0']

    g = {'2': ['1', '3'], '1 3': ['2', '1', '2']}

    g = remove_self_cycle(g, '1 3')

    assert g['1 3'] == ['2', '2'], g

    g = {'1 2': ['0', '4'],
         '3': ['4', '5'],
         '5': ['6', '7']
         }

    g = merge_graph_nodes(g, '1 2', '3')

    assert '1 2 3' in g
    assert len(g) == 2
    assert sorted(g['1 2 3']) == sorted(['0', '4', '4', '5'])

    g = {'1 3': ['2', '3', '1', '2'], '2': ['1', '3']}
    g = remove_self_cycle(g, '1 3')
    assert sorted(g['1 3']) == ['2', '2']

    g = {'1': ['2', '3'],
         '2': ['1', '3'],
         '3': ['1', '2'],
         }

    g = random_contract_graph(g, dependancy_injection=random_generator())
    all_keys = list(g.keys())
    a, b = get_vertex_edges(g, all_keys[0]), get_vertex_edges(g, all_keys[1])
    assert len(a) == 2

    print('test done!')

    graph = {str(ii+1) : line.strip().split('\t') for ii, line in enumerate(open('data/kargerMinCut.txt'))}

    g = random_contract_graph(graph, verbose=True)
    print(len(get_vertex_edges(g, list(g.keys())[0])))



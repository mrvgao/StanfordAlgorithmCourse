import unittest
from utils.utils import sorted_list_with_tuple
from graph import Graph
from random_contract import random_select_vertex
from random_contract import random_contract_one_pass
from random_contract import random_contract
from random import Random
from itertools import repeat


class GraphTestCase(unittest.TestCase):
    def test_create_empty_graph(self):
        g = Graph()
        self.assertEqual(list(g.adjacency.keys()), [])

    def test_create_base_nodes(self):
        vertices_nodes = [0, 1, 2, 3]
        g = Graph(vertices_nodes)
        self.assertEqual(sorted(list(g.adjacency.keys())), sorted(vertices_nodes))

    def test_get_vertices(self):
        g = Graph()
        self.assertEqual(g.get_vertices(), [])

    def test_create_connection(self):
        vertices_nodes = [0, 1, 2, 3]
        g = Graph(vertices_nodes)

        g.connect(0, 1)

        self.assertEqual(g.adjacency[0], {1: 1})
        self.assertEqual(g.adjacency[1], {0: 1})


class GraphOpTestCase(unittest.TestCase):
    def setUp(self):
        vertices_nodes = [0, 1, 2, 3]
        vertices_connections = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
        self.g = Graph(vertices_nodes, vertices_connections)

    def test_create_base_node_and_connections(self):
        self.assertEqual(self.g.adjacency[0], {1: 1, 2: 1, 3: 1})
        self.assertEqual(self.g.adjacency[1], {0: 1, 2: 1})

    def test_add_new_vertex(self):
        self.assertNotIn(5, self.g.adjacency)

        self.g.add_vertex(5)

        self.assertIn(5, self.g.adjacency)

        self.g.add_vertex((1, 3))

        self.assertIn((1, 3), self.g.adjacency)

    def test_add_new_connection(self):
        vertices_nodes = [0, 1, 2]
        vertices_connections = [(0, 1)]

        g = Graph(vertices_nodes, vertices_connections)

        self.assertEqual(g.adjacency[0], {1: 1})
        self.assertEqual(g.adjacency[1], {0: 1})

        g.connect(1, 2)

        self.assertEqual(g.adjacency[1], {0: 1, 2: 1})
        self.assertEqual(g.adjacency[2], {1: 1})

    def test_disconnect(self):
        self.assertEqual(self.g.adjacency[0], {1: 1, 2: 1, 3: 1})
        self.assertEqual(self.g.adjacency[2], {0: 1, 1: 1, 3: 1})

        self.g.disconnect(0, 2)

        self.assertEqual(self.g.adjacency[0], {1: 1, 3: 1})
        self.assertEqual(self.g.adjacency[2], {1: 1, 3: 1})

        self.g.disconnect(0, 9)

        self.assertEqual(self.g.adjacency[0], {1: 1, 3: 1})
        self.assertEqual(self.g.adjacency[2], {1: 1, 3: 1})

    def test_is_connected(self):
        self.assertTrue(self.g.is_connected(1, 0))
        self.assertFalse(self.g.is_connected(1, 3))

    def test_merge_vertices_get_new_vertex(self):
        vertices = [1, 2]
        self.assertEqual(Graph.merge_vertices_get_new_vertex(vertices), (1, 2))
        vertices = [(1, 2), 3]
        self.assertEqual(Graph.merge_vertices_get_new_vertex(vertices), (1, 2, 3))

    def test_replace_vertex_adjacent(self):
        self.g.replace_adjacent(0, 2, 4)

        self.assertEqual(self.g.adjacency[0], {1: 1, 3: 1, 4: 1})
        self.assertIn(4, self.g.adjacency)
        self.assertEqual(self.g.adjacency[4], {0: 1})
        self.assertEqual(self.g.adjacency[1], {0: 1, 2: 1})
        self.assertEqual(self.g.adjacency[3], {0: 1, 2: 1})

    def test_change_vertex_name(self):

        self.g.change_vertex_name(0, (0, 1))
        self.assertEqual(self.g.adjacency[(0, 1)], {1:1, 2:1, 3:1})
        self.assertNotIn(0, self.g.adjacency)

        self.assertEqual(self.g.adjacency[1], {(0, 1): 1, 2: 1})
        self.assertEqual(self.g.adjacency[2], {1: 1, (0, 1): 1, 3: 1})
        self.assertEqual(self.g.adjacency[3], {(0, 1): 1, 2: 1})

    def test_change_vertex_name_with_new_name_already_exist(self):
        self.g.change_vertex_name(0, 1)
        self.assertEqual(self.g.adjacency[1], {1: 1, 2: 2, 3: 1})
        self.assertNotIn(0, self.g.adjacency)

    def test_change_vertex_with_4_nodes(self):
        self.assertEqual(self.g.adjacency[0], {1:1, 2:1, 3:1})
        self.assertEqual(self.g.adjacency[1], {0:1, 2:1})
        self.assertEqual(self.g.adjacency[2], {0:1, 1:1, 3:1})
        self.assertEqual(self.g.adjacency[3], {0:1, 2:1})

        self.g.change_vertex_name(0, (0, 1))
        self.assertNotIn(0, self.g.adjacency)
        self.assertEqual(self.g.adjacency[(0, 1)], {1:1, 2:1, 3:1})
        self.assertEqual(self.g.adjacency[1], {(0, 1):1, 2:1})
        self.assertEqual(self.g.adjacency[2], {(0, 1):1, 1:1, 3:1})
        self.assertEqual(self.g.adjacency[3], {(0, 1):1, 2:1})

    def test_change_name_with_self_cycle(self):
        self.g.change_vertex_name(0, (0, 1))
        self.g.connect((0, 1), (0, 1), degree=2)
        self.assertEqual(self.g.adjacency[(0, 1)], {1: 1, 2: 1, 3: 1, (0, 1): 2})
        self.assertEqual(self.g.adjacency[1], {(0, 1): 1, 2: 1})
        self.assertEqual(self.g.adjacency[2], {(0, 1): 1, 1: 1, 3: 1})
        self.assertEqual(self.g.adjacency[3], {(0, 1): 1, 2: 1})

    def test_merge_vertices_with_two_nodes(self):
        vertices = [0, 1]
        connection = [(0, 1)]

        g = Graph(nodes=vertices, connections=connection)
        g.merge_vertices([0, 1])
        self.assertEqual(g.adjacency[(0, 1)], {(0, 1): 1})

    def test_merge_vertices_with_4_vertices(self):

        self.g.merge_vertices([0, 1])

        self.assertIn((0, 1), self.g.adjacency)
        self.assertNotIn(0, self.g.adjacency)
        self.assertNotIn(1, self.g.adjacency)

        self.assertEqual(self.g.adjacency[(0, 1)], {(0, 1): 1, 2: 2, 3: 1})

        self.assertEqual(self.g.adjacency[3], {(0, 1): 1, 2: 1})
        self.assertEqual(self.g.adjacency[2], {(0, 1): 2, 3: 1})

    def test_merge_with_continue_merge(self):
        vertices_num = len(self.g.get_vertices())

        self.g.merge_vertices([0, 1])
        self.assertEqual(len(self.g.get_vertices()), vertices_num - 1)

        print(self.g)

        self.g.merge_vertices([(0, 1), 2])

        self.assertEqual(len(self.g.get_vertices()), vertices_num - 2, msg=self.g.adjacency)

        self.assertIn((0, 1, 2), self.g.adjacency)
        self.assertNotIn((0, 1), self.g.adjacency)

        result = {3: 2, (0, 1, 2): 3}
        self.assertEqual(self.g.adjacency[(0, 1, 2)], result)

        print(self.g)

    def test_remove_self_cycle(self):
        vertices = [0, 1, 2]
        connections = [(0, 0), (1, 0), (0, 1), (1, 1)]

        g = Graph(vertices, connections)

        self.assertEqual(g.adjacency[0], {0: 1, 1: 2})

        g.remove_one_vertex_self_cycle(0)

        self.assertEqual(g.adjacency[0], {1: 2})

        vertices = [0, 1, 2]
        connections = [(0, 0), (0, 0), (1, 0), (0, 1), (1, 1)]
        g = Graph(vertices, connections)
        g.remove_one_vertex_self_cycle(0)
        self.assertEqual(g.adjacency[0], {1: 2})


class RandomContractTestCase(unittest.TestCase):
    def setUp(self):
        vertices_nodes = [0, 1, 2, 3]
        vertices_connections = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
        self.g = Graph(vertices_nodes, vertices_connections)

    def test_select_vertex(self):
        vertex = random_select_vertex(self.g, num=1)

        self.assertIn(vertex, self.g.get_vertices())

        vertices = random_select_vertex(self.g, num=2)

        self.assertIn(vertices[0], self.g.get_vertices())
        self.assertIn(vertices[1], self.g.get_vertices())

    def test_random_contract(self):

        g = random_contract_one_pass(self.g)

        vertices = g.get_vertices()

        self.assertEqual(len(vertices), 2)
        self.assertEqual(len(g.adjacency[vertices[0]]), len(g.adjacency[vertices[1]]))
        self.assertEqual(list(map(lambda x: x == vertices[0], g.adjacency[vertices[1]])), [True] * len(g.adjacency[vertices[1]]))
        self.assertEqual(list(map(lambda x: x == vertices[1], g.adjacency[vertices[0]])), [True] * len(g.adjacency[vertices[0]]))

    def test_complicate_graph_contract(self):
        # given more complicated graph structure to test the random contract.

        def get_random_generator(size=100):
            for i in repeat(range(size)):
                yield i

        for i in range(100):
            print('i == {}'.format(i))

            size = 140
            seed = next(get_random_generator(size))

            random = Random(seed)

            print('random seed: {}'.format(seed))

            vertex_num = random.randrange(size) + 2
            parirs_num = random.randrange(int(size * 1.5)) + 2

            nodes = list(range(vertex_num))
            pairs = [(random.choice(nodes), random.choice(nodes)) for _ in range(parirs_num)]
            pairs = list(filter(lambda a_b: a_b[0] != a_b[1], pairs))

            g = Graph(nodes, pairs)

            print(vertex_num)
            print(parirs_num)

            random_contract_one_pass(g)

            vertices = g.get_vertices()
            no_empty_vertices = list(filter(lambda v: len(g.adjacency[v]), vertices))

            self.assertEqual(len(no_empty_vertices), 2)
            one_vertex, another_vertex = no_empty_vertices

            self.assertEqual([one_vertex], list(g.adjacency[another_vertex].keys()))
            self.assertEqual([another_vertex], list(g.adjacency[one_vertex].keys()))
            self.assertEqual(g.adjacency[one_vertex][another_vertex], g.adjacency[another_vertex][one_vertex])

    def test_get_min_cut(self):
        vertices_nodes = [0, 1, 2, 3]
        vertices_connections = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
        graph = Graph(vertices_nodes, vertices_connections)
        min_cut_num = random_contract(graph, verboes=True)

        self.assertEqual(min_cut_num, 2)

        nodes = [1, 2, 3, 4, 5, 6, 7, 8]
        connections = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1), (2, 7),
                       (3, 6), (4, 7), (6, 8)]

        # g = Graph(nodes, connections)
        self.assertEqual(random_contract(Graph(nodes, connections), verboes=True), 1)

        nodes = list(range(200))

        def create_cycle(cycle_list):
            result = [(e, cycle_list[i+1]) if i < len(cycle_list) - 1 else (e, 0) for i, e in enumerate(cycle_list)]
            return result

        cycle_1 = create_cycle(nodes[:100])
        cycle_2 = create_cycle([nodes[0]] + nodes[100:])  # remove the last one connect to zero.
        cycle_2.pop()

        print(cycle_1)
        print(cycle_2)
        connections = cycle_1 + cycle_2

        graph = Graph(nodes, connections)
        self.assertEqual(random_contract(graph, verboes=True), 1)


if __name__ == '__main__':
    unittest.main()

import unittest
from utils.utils import sorted_list_with_tuple
from graph import Graph


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

        self.assertEqual(g.adjacency[0], [1])
        self.assertEqual(g.adjacency[1], [0])


class GraphOpTestCase(unittest.TestCase):
    def setUp(self):
        vertices_nodes = [0, 1, 2, 3]
        vertices_connections = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
        self.g = Graph(vertices_nodes, vertices_connections)

    def test_create_base_node_and_connections(self):
        self.assertEqual(sorted(self.g.adjacency[0]), sorted([1, 2, 3]))
        self.assertEqual(sorted(self.g.adjacency[1]), sorted([0, 2]))

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

        self.assertEqual(g.adjacency[0], [1])
        self.assertEqual(g.adjacency[1], [0])

        g.connect(1, 2)

        self.assertEqual(sorted(g.adjacency[1]), sorted([0, 2]))
        self.assertEqual(sorted(g.adjacency[2]), sorted([1]))

    def test_disconnect(self):
        self.assertEqual(sorted(self.g.adjacency[0]), sorted([1, 2, 3]))
        self.assertEqual(sorted(self.g.adjacency[2]), sorted([0, 1, 3]))

        self.g.disconnect(0, 2)

        self.assertEqual(sorted(self.g.adjacency[0]), sorted([1, 3]))
        self.assertEqual(sorted(self.g.adjacency[2]), sorted([1, 3]))

        self.g.disconnect(0, 9)

        self.assertEqual(sorted(self.g.adjacency[0]), sorted([1, 3]))
        self.assertEqual(sorted(self.g.adjacency[2]), sorted([1, 3]))

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

        self.assertEqual(sorted(self.g.adjacency[0]), [1, 3, 4])
        self.assertIn(4, self.g.adjacency)
        self.assertEqual(self.g.adjacency[4], [0])
        self.assertEqual(sorted(self.g.adjacency[1]), [0, 2])
        self.assertEqual(sorted(self.g.adjacency[3]), [0, 2])

    def test_change_vertex_name(self):

        zero_previous_connected = self.g.adjacency[0]
        self.g.change_vertex_name(0, (0, 1))
        self.assertEqual(self.g.adjacency[(0, 1)], zero_previous_connected)
        self.assertNotIn(0, self.g.adjacency)

        s = sorted_list_with_tuple
        self.assertEqual(s(self.g.adjacency[1]), s([(0, 1), 2]))
        self.assertEqual(s(self.g.adjacency[2]), s([1, (0, 1), 3]))
        self.assertEqual(s(self.g.adjacency[3]), s([(0, 1), 2]))

    def test_change_vertex_name_with_new_name_already_exist(self):
        self.g.change_vertex_name(0, 1)

        s = sorted_list_with_tuple
        self.assertEqual(s(self.g.adjacency[1]), s([1, 2, 1, 2, 3]))

    def test_merge_vertices_with_two_nodes(self):
        vertices = [0, 1]
        connection = [(0, 1)]

        g = Graph(nodes=vertices, connections=connection)
        g.merge_vertices([0, 1])
        self.assertEqual(g.adjacency[(0, 1)], [])

    def test_merge_vertices_with_4_vertices(self):

        self.g.merge_vertices([0, 1])

        self.assertIn((0, 1), self.g.adjacency)
        self.assertNotIn(0, self.g.adjacency)
        self.assertNotIn(1, self.g.adjacency)

        s = sorted_list_with_tuple

        self.assertEqual(s(self.g.adjacency[(0, 1)]),
                         s([2, 3, 2]), self.g)

        self.assertEqual(s(self.g.adjacency[3]), s([(0, 1), 2]))
        self.assertEqual(s(self.g.adjacency[2]), s([(0, 1), (0, 1), 3]))

    def test_remove_self_cycle(self):
        vertices = [0, 1, 2]
        connections = [(0, 0), (1, 0), (0, 1), (1, 1)]

        g = Graph(vertices, connections)

        self.assertEqual(g.adjacency[0], [0, 0, 1, 1])

        g.remove_one_vertex_self_cycle(0)

        self.assertEqual(g.adjacency[0], [1, 1])

    def test_merge_with_continue_merge(self):
        s = sorted_list_with_tuple
        self.g.merge_vertices([0, 1])

        self.g.merge_vertices([(0, 1), 2])

        self.assertIn((0, 1, 2), self.g.adjacency)
        self.assertNotIn((0, 1), self.g.adjacency)
        self.assertEqual(s(self.g.adjacency[(0, 1, 2)]),
                         s(([3, 3])))

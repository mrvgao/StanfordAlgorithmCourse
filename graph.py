from functools import reduce
import operator as op


class Graph:
    def __init__(self, nodes=[], connections=[]):
        self.adjacency = {v: [] for v in nodes}

        for c in connections:
            a, b = c
            self.connect(a, b)

    def get_vertices(self):
        return list(self.adjacency.keys())

    def add_vertex(self, new_vertex):
        if new_vertex not in self.adjacency:
            self.adjacency[new_vertex] = []

    def connect(self, a, b):

        if a not in self.adjacency: self.add_vertex(a)

        if b not in self.adjacency: self.add_vertex(b)

        self.adjacency[a].append(b)
        self.adjacency[b].append(a)

    def __remove_from(self, need_deleted, origin):
        if origin in self.adjacency and need_deleted in self.adjacency[origin]:
            self.adjacency[origin].remove(need_deleted)

    def disconnect(self, a, b):
        self.__remove_from(a, b)
        self.__remove_from(b, a)

    def is_connected(self, a, b):
        return b in self.adjacency[a] and a in self.adjacency[b]

    @staticmethod
    def merge_vertices_get_new_vertex(vertices):
        new_vertex = []

        for v in vertices:
            if isinstance(v, tuple):
                new_vertex += list(v)
            else:
                new_vertex += [v]

        new_vertex = tuple(new_vertex)
        return new_vertex

    def replace_adjacent(self, vertex, previous_adjacent, new_adjacent):
        self.disconnect(vertex, previous_adjacent)
        self.connect(vertex, new_adjacent)

    def remove_one_vertex_self_cycle(self, vertex):
        self.adjacency[vertex] = list(filter(lambda x: x != vertex, self.adjacency[vertex]))

    def change_vertex_name(self, old_vertex, new_name):
        connected_with_vertex = self.adjacency[old_vertex]

        for v in connected_with_vertex:
            self.adjacency[v] = [new_name if name == old_vertex else name for name in self.adjacency[v]]

        if new_name not in self.adjacency: self.adjacency[new_name] = []

        self.adjacency[new_name] += connected_with_vertex

        del self.adjacency[old_vertex]

    def merge_vertices(self, need_merged_vertices):
        new_vertex = Graph.merge_vertices_get_new_vertex(need_merged_vertices)

        for v in need_merged_vertices:
            self.change_vertex_name(v, new_vertex)

        self.remove_one_vertex_self_cycle(new_vertex)

    def __str__(self):
        return self.adjacency


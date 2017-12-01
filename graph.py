from utils.utils import replace_element_quickly
import copy
from collections import Counter


class Graph:
    def __init__(self, nodes=[], connections=[]):
        self.adjacency = {v: Counter({}) for v in nodes}

        for c in connections:
            a, b = c
            self.connect(a, b)

    def get_vertices(self):
        return list(self.adjacency.keys())

    def add_vertex(self, new_vertex):
        if new_vertex not in self.adjacency:
            self.adjacency[new_vertex] = {}

    def connect(self, a, b, degree=1):

        if a not in self.adjacency: self.add_vertex(a)

        if b not in self.adjacency: self.add_vertex(b)

        self.adjacency[a][b] = self.adjacency[a].setdefault(b, 0) + degree

        if a != b:
            self.adjacency[b][a] = self.adjacency[b].setdefault(a, 0) + degree

    def __remove_from(self, need_deleted, origin, degree=1):
        if origin in self.adjacency and need_deleted in self.adjacency[origin]:
            if need_deleted in self.adjacency[origin]:
                if self.adjacency[origin][need_deleted] - degree <= 0: del self.adjacency[origin][need_deleted]
                else:
                    self.adjacency[origin][need_deleted] -= degree

    def disconnect(self, a, b, degree=1):
        self.__remove_from(a, b, degree=degree)
        self.__remove_from(b, a, degree=degree)

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
        if vertex in self.adjacency and vertex in self.adjacency[vertex]:
            del self.adjacency[vertex][vertex]

    def change_vertex_name(self, old_vertex, new_name):
        old_vertex_adjacencies = self.adjacency[old_vertex].keys()
        for previous_connected in list(old_vertex_adjacencies):
            if previous_connected != old_vertex:
                connected_with_new_name = previous_connected
            else:
                connected_with_new_name = new_name

            degree = self.adjacency[previous_connected][old_vertex]
            self.connect(connected_with_new_name, new_name, degree=degree)
            self.disconnect(previous_connected, old_vertex, degree=degree)

            if len(self.adjacency[old_vertex]) == 0:
                del self.adjacency[old_vertex]

        assert old_vertex not in self.adjacency

    def merge_vertices(self, need_merged_vertices):
        new_vertex = Graph.merge_vertices_get_new_vertex(need_merged_vertices)

        for v in need_merged_vertices:
            self.change_vertex_name(v, new_vertex)

        return new_vertex

    def __str__(self):
        return str(self.adjacency)


"""
Implement the heap data structure.
"""


class Heap:
    def __init__(self, array=[]):
        self._array = []
        self.k_v = {}
        for e in array: self.insert(e)

    def array(self, item, with_key=False):
        try:
            if not with_key:
                return self._array[item][1]
            else:
                return self._array[item]
        except TypeError:
            return self._array[item]
        except IndexError:
            return None

    def insert(self, element):
        self._array.append(element)

        try:
            iter(element)
            self.k_v[element[0]] = element[1]
        except TypeError:
            pass

        index = len(self._array) - 1
        while index > 0 and self.array(index) < self.array(self.parent(index)):
            self.swap(index, self.parent(index))
            index = self.parent(index)

    def pop(self, with_key=False, index=0):
        if len(self._array) <= 0: return None
        root = self.array(index, with_key)

        self.swap(index, len(self._array) - 1)
        self._array.pop()

        while any([self.array(c) < self.array(index) for c in self.children(index) if c is not None]):
            c1, c2 = self.children(index)
            swap_index = c1 or c2  # get the not none index

            if c1 is not None and c2 is not None:
                swap_index = min([c1, c2], key=lambda x: self.array(x))

            self.swap(index, swap_index)

            index = swap_index

        return root

    def parent(self, i):
        if i == 0 or i >= len(self._array):
            return None
        else:
            p_index = (i-1) // 2
            return p_index

    def children(self, i):
        children_i = [i * 2 + 1, i * 2 + 2]

        if children_i[0] + 1 > len(self._array):
            children_i[0] = None
        if children_i[1] + 1 > len(self._array):
            children_i[1] = None

        return children_i[0], children_i[1]

    def swap(self, i, j):
        self._array[i], self._array[j] = self._array[j], self._array[i]


heap = Heap()

heap._array = [1, 2, 3, 4, 5, 6, 7, 9]
'''
                  1
                2   3
            4    5 6    7
        9
'''
assert heap.parent(0) is None
assert heap.parent(1) == 0
assert heap.parent(4) == 1
assert heap.parent(10) is None

assert heap.children(0) == (1, 2)
assert heap.children(3) == (7, None)
assert heap.children(4) == (None, None)

heap.swap(0, 1)

assert heap._array == [2, 1, 3, 4, 5, 6, 7, 9]

heap = Heap()

heap.insert(1)
heap.insert(0)

assert heap._array == [0, 1], heap.array

heap.insert(4)

assert heap._array == [0, 1, 4]

heap.insert(3)
heap.insert(2)

heap.insert(3)

assert heap._array == [0, 1, 3, 3, 2, 4]

heap.insert(2)

assert heap._array == [0, 1, 2, 3, 2, 4, 3]

heap.insert(-1)

assert heap._array == [-1, 0, 2, 1, 2, 4, 3, 3]

heap = Heap([1, 0, 4, 3, 2, 3, 2, -1])
assert heap._array == [-1, 0, 2, 1, 2, 4, 3, 3]

v = heap.pop()

assert v == -1
assert heap._array == [0, 1, 2, 3, 2, 4, 3], heap.array

v = heap.pop()

assert v == 0

assert heap._array == [1, 2, 2, 3, 3, 4]

heap = Heap([('a', 1), ('b', 0), ('c', 4), ('d', 3), ('e', 2), ('f', 3), ('g', 2), ('h', -1)])

assert [v for k, v in heap._array] == [-1, 0, 2, 1, 2, 4, 3, 3]

assert heap.pop(with_key=True) == ('h', -1)
assert heap.pop(with_key=True) == ('b', 0)

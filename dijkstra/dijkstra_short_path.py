from collections import defaultdict
from heap.heap import Heap

"""
When using the 'naive' implementation of Dijstra shortest_path, the running time is 
O(mn), where m is the edges number and n is vertices number.
"""


def short_path(graph, start, end):
    processed = set()
    processed.add(start)

    shortest_path = defaultdict(lambda : float('inf'))
    predecessor = defaultdict(list)
    shortest_path[start] = 0

    heap = Heap(graph[start])

    while len(processed) < len(graph):
        w_star, w_star_dis = heap.pop(with_key=True)
        shortest_path[w_star] = w_star_dis

        for v, v_dis in graph[w_star]:
            if v in processed: continue

            try:
                key_v = heap.pop(key=v)
            except KeyError:
                key_v = float('inf')

            key_v = min(key_v, shortest_path[w_star] + v_dis)

            heap.insert((v, key_v))

        processed.add(w_star)
        predecessor[end].append(w_star)


        # v_w_pair = []
        # for v in processed:
        #     v_w_pair += [(v, w, shortest_path[v] + dis_w) for w, dis_w in graph[v] if w not in processed]
        #
        # v_star, w_star, w_star_dis = min(v_w_pair, key=lambda x: x[2])
        #
        # processed.add(w_star)
        # shortest_path[w_star] = w_star_dis
        # predecessor[w_star] = predecessor[v_star] + [w_star]

        if w_star == end: break

    return shortest_path[end], predecessor[end]


G = {
    'a': [('b', 1), ('c', 4), ('d', 5)],
    'b': [('a', 1), ('c', 1)],
    'c': [('b', 1), ('d', 1)],
    'd': [('c', 1), ('a', 5)]
}

print(short_path(G, 'a', 'd'))


if __name__ == '__main__':
    g = {}
    for line in open('../data/dijkstraData.txt'):
        split = line.split()
        g[split[0]] = [v_length.split(',') for v_length in split[1:]]
        g[split[0]] = [(v, int(length)) for v, length in g[split[0]]]


assert len(g) == 200

test_data = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]

with open('../data/dijkstra_ans.txt', 'w') as f:
    for d in test_data:
        print('data : {}'.format(d))
        sp = short_path(g, '1', str(d))
        print(sp)
        f.write('{}: {}\n'.format(d, sp))

from collections import defaultdict

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
    while len(processed) < len(graph):
        v_w_pair = []
        for v in processed:
            v_w_pair += [(v, w, shortest_path[v] + dis_w) for w, dis_w in graph[v] if w not in processed]

        v_star, w_star, w_star_dis = min(v_w_pair, key=lambda x: x[2])

        processed.add(w_star)
        shortest_path[w_star] = w_star_dis
        predecessor[w_star] = predecessor[v_star] + [w_star]

        if w_star == end: break

    return shortest_path[end], predecessor[end]


G = {
    'a': [('b', 1), ('d', 3), ('c', 2)],
    'b': [('a', 1), ('d', 1)],
    'c': [('a', 2), ('d', 1), ('e', 3)],
    'd': [('b', 1), ('a', 3), ('c', 1), ('e', 1)],
    'e': [('d', 1), ('c', 2)]
}

print(short_path(G, 'a', 'e'))


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
        f.write('{}: {}'.format(d, sp))

from collections import defaultdict


def short_path(graph, start, end):
    processed = set()
    processed.add(start)

    shortest_path = defaultdict(lambda : float('inf'))
    predecessor = defaultdict(list)
    shortest_path[start] = 0

    while len(processed) < len(graph):
        w_star = None

        X = processed - set([])
        for v in X:
            v_w_distances = [(w, shortest_path[v] + v_w)
                             for w, v_w in graph[v]
                             if w not in processed
                            ]
            if len(v_w_distances) > 0:
                w_star, w_star_distance = min(v_w_distances, key=lambda x: x[1])
                if w_star_distance < shortest_path[w_star]:
                    shortest_path[w_star] = w_star_distance
                    predecessor[w_star] = predecessor[v] + [w_star]

            if w_star is not None:
                processed.add(w_star)

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


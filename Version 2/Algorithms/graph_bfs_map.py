import time
from collections import deque

def graph_bfs_map(start, end, G):
    start_time = time.time()

    queue = deque([start])
    visited = set([start])
    parent = {}
    visited_order = []

    while queue:
        node = queue.popleft()
        visited_order.append(node)

        if node == end:
            return {
                "visited_order": visited_order,
                "path": reconstruct(parent, start, end),
                "time_taken": time.time() - start_time
            }

        for neighbor in G.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)

    return None


def reconstruct(parent, start, end):
    path = []
    cur = end

    while cur != start:
        if cur not in parent:
            return []
        path.append(cur)
        cur = parent[cur]

    path.append(start)
    path.reverse()
    return path
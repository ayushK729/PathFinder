import time

def graph_dfs_map(start, end, G):
    start_time = time.time()

    stack = [start]
    visited = set()
    parent = {}
    visited_order = []

    while stack:

        current = stack.pop()

        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)

        if current == end:
            return {
                "visited_order": visited_order,
                "path": reconstruct(parent, start, end),
                "time_taken": time.time() - start_time
            }

        for neighbor in G.neighbors(current):
            if neighbor not in visited:
                parent[neighbor] = current
                stack.append(neighbor)

    return None


def reconstruct(parent, start, end):
    path = []
    cur = end

    while cur != start:
        path.append(cur)
        cur = parent[cur]

    path.append(start)
    path.reverse()
    return path
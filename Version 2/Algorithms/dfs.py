from collections import deque
import time
from Algorithms.grid_utility import get_neighbors, reconstruct_path

def dfs(start, end, grid):
    import time
    start_time = time.time()

    stack = [start]
    visited = set([start])
    parent = {}
    visited_order = []

    while stack:
        current = stack.pop()
        visited_order.append(current)

        if current == end:
            path = reconstruct_path(parent, start, end)
            return {
                "visited_order": visited_order,
                "path": path,
                "time_taken": time.time() - start_time
            }

        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    return None
import heapq
from Algorithms.grid_utility import get_neighbors, reconstruct_path

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan


def astar(start, end, grid):
    import time
    start_time = time.time()

    pq = [(0, start)]
    parent = {}
    g_cost = {start: 0}
    visited_order = []

    while pq:
        _, current = heapq.heappop(pq)
        visited_order.append(current)

        if current == end:
            path = reconstruct_path(parent, start, end)
            return {
                "visited_order": visited_order,
                "path": path,
                "time_taken": time.time() - start_time
            }

        for neighbor in get_neighbors(current, grid):
            temp_g = g_cost[current] + 1

            if neighbor not in g_cost or temp_g < g_cost[neighbor]:
                g_cost[neighbor] = temp_g
                f_cost = temp_g + heuristic(neighbor, end)

                parent[neighbor] = current
                heapq.heappush(pq, (f_cost, neighbor))

    return None
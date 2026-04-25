from Algorithms.grid_utility import get_neighbors, reconstruct_path
import heapq
import time

# Heuristic function (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def greedy_bfs(start, end, grid):
    start_time = time.time()

    # Priority Queue: (priority, node)
    pq = [(0, start)]

    visited = set()
    parent = {}
    visited_order = []

    while pq:
        _, current = heapq.heappop(pq)

        # Skip if already processed
        if current in visited:
            continue

        # Mark visited ONLY when popped
        visited.add(current)
        visited_order.append(current)

        # Goal check
        if current == end:
            path = reconstruct_path(parent, start, end)
            return {
                "visited_order": visited_order,
                "path": path,
                "time_taken": time.time() - start_time
            }

        # Explore neighbors
        for neighbor in get_neighbors(current, grid):
            if neighbor not in visited:
                parent[neighbor] = current
                priority = heuristic(neighbor, end)
                heapq.heappush(pq, (priority, neighbor))

    return None
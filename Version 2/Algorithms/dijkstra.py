from Algorithms.grid_utility import get_neighbors, reconstruct_path
import heapq

def dijkstra(start, end, grid):
    import time
    start_time = time.time()

    pq = [(0, start)]
    visited = set()
    parent = {}
    dist = {start: 0}
    visited_order = []

    while pq:
        cost, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)

        if current == end:
            path = reconstruct_path(parent, start, end)
            return {
                "visited_order": visited_order,
                "path": path,
                "time_taken": time.time() - start_time
            }

        for neighbor in get_neighbors(current, grid):
            new_cost = cost + 1

            if neighbor not in dist or new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    return None